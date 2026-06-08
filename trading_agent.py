#!/usr/bin/env python3
"""
Trading Intelligence Agent
- Webhook server: receives TradingView alerts on POST /webhook
- News: fetches latest headlines via NewsAPI
- Analysis: sends signal + news to Claude for a structured trade report
- Logging: writes each report to a Notion database
- Schedule: re-runs analysis on the watchlist every Monday at 8:00 AM
"""

import json
import logging
import threading
import time
from datetime import datetime

import anthropic
import requests
import schedule
from flask import Flask, jsonify, request

# ──────────────────────────────────────────────────────────────────────────────
# Configuration — replace with your real keys or load from environment variables
# ──────────────────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY  = "your_anthropic_key_here"
NEWS_API_KEY       = "your_newsapi_key_here"
NOTION_API_KEY     = "your_notion_key_here"
NOTION_DATABASE_ID = "your_notion_database_id_here"

# Webhook server settings
WEBHOOK_HOST = "0.0.0.0"
WEBHOOK_PORT = 5000

# Tickers to analyze on the Monday 8 AM scheduled run (no incoming signal needed)
WATCHLIST = ["AAPL", "TSLA", "NVDA", "SPY", "QQQ", "BTC-USD", "ETH-USD"]

# ──────────────────────────────────────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# API clients
# ──────────────────────────────────────────────────────────────────────────────
app    = Flask(__name__)
claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


# ──────────────────────────────────────────────────────────────────────────────
# Step 1 – Fetch news
# ──────────────────────────────────────────────────────────────────────────────
def fetch_news(ticker: str, max_articles: int = 5) -> list[dict]:
    """Return the latest news articles for a ticker from NewsAPI."""
    try:
        resp = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q":        ticker,
                "sortBy":   "publishedAt",
                "pageSize": max_articles,
                "language": "en",
                "apiKey":   NEWS_API_KEY,
            },
            timeout=10,
        )
        resp.raise_for_status()
        articles = resp.json().get("articles", [])
        return [
            {
                "title":        a.get("title", ""),
                "description":  a.get("description", ""),
                "source":       a.get("source", {}).get("name", ""),
                "published_at": a.get("publishedAt", ""),
            }
            for a in articles
        ]
    except Exception as exc:
        log.error("NewsAPI error for %s: %s", ticker, exc)
        return []


# ──────────────────────────────────────────────────────────────────────────────
# Step 2 – Claude analysis
# ──────────────────────────────────────────────────────────────────────────────
def analyze_with_claude(ticker: str, signal_data: dict, news: list[dict]) -> dict:
    """
    Send ticker + signal + news to Claude Opus 4.8 and return a structured
    trade report as a Python dict.
    """
    news_text = "\n".join(
        f"- [{a['source']}] {a['title']}: {a['description']}"
        for a in news
    ) or "No recent news available."

    prompt = f"""You are a professional trading analyst. Analyze the following trading signal and recent news, then produce a concise trade report.

TICKER: {ticker}
SIGNAL DATA:
{json.dumps(signal_data, indent=2)}

RECENT NEWS:
{news_text}

Return ONLY a valid JSON object — no markdown, no prose, no explanation — using exactly this schema:
{{
  "ticker":             "{ticker}",
  "action":             "BUY | SELL | HOLD",
  "entry_price":        <float or null>,
  "stop_loss":          <float or null>,
  "take_profit":        <float or null>,
  "position_size_pct":  <float 0-100, recommended % of portfolio>,
  "risk_reward_ratio":  <float or null>,
  "confidence":         "HIGH | MEDIUM | LOW",
  "reasoning":          "<2-3 sentence explanation of the trade rationale>",
  "news_sentiment":     "BULLISH | BEARISH | NEUTRAL",
  "news_summary":       "<1 sentence summary of the most relevant news>"
}}"""

    try:
        message = claude.messages.create(
            model="claude-opus-4-8",
            max_tokens=1024,
            thinking={"type": "adaptive"},          # let Claude decide how much to think
            output_config={"effort": "high"},       # high intelligence for trade decisions
            messages=[{"role": "user", "content": prompt}],
        )

        # Extract text from the response (skip thinking blocks)
        raw = ""
        for block in message.content:
            if block.type == "text":
                raw = block.text.strip()
                break

        # Strip accidental markdown code fences
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

        return json.loads(raw)

    except Exception as exc:
        log.error("Claude analysis error for %s: %s", ticker, exc)
        return {
            "ticker":    ticker,
            "action":    "ERROR",
            "reasoning": str(exc),
            "error":     True,
        }


# ──────────────────────────────────────────────────────────────────────────────
# Step 3 – Log to Notion
# ──────────────────────────────────────────────────────────────────────────────
def log_to_notion(report: dict, signal_data: dict) -> bool:
    """
    Create a new page in the Notion database with the trade report.

    Your Notion database needs these properties (exact names matter):
      Name             – Title
      Ticker           – Rich text
      Action           – Select  (BUY / SELL / HOLD / ERROR)
      Confidence       – Select  (HIGH / MEDIUM / LOW)
      News Sentiment   – Select  (BULLISH / BEARISH / NEUTRAL)
      Entry Price      – Number
      Stop Loss        – Number
      Take Profit      – Number
      Position Size %  – Number
      Risk/Reward      – Number
      Date             – Date
    """
    ticker = report.get("ticker", "UNKNOWN")
    action = report.get("action", "UNKNOWN")
    now    = datetime.utcnow().isoformat() + "Z"

    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {
                "title": [{"text": {"content": f"{ticker} — {action} — {now[:10]}"}}]
            },
            "Ticker":           {"rich_text": [{"text": {"content": ticker}}]},
            "Action":           {"select": {"name": action}},
            "Confidence":       {"select": {"name": report.get("confidence", "LOW")}},
            "News Sentiment":   {"select": {"name": report.get("news_sentiment", "NEUTRAL")}},
            "Entry Price":      {"number": report.get("entry_price")},
            "Stop Loss":        {"number": report.get("stop_loss")},
            "Take Profit":      {"number": report.get("take_profit")},
            "Position Size %":  {"number": report.get("position_size_pct")},
            "Risk/Reward":      {"number": report.get("risk_reward_ratio")},
            "Date":             {"date": {"start": now}},
        },
        # Add body blocks with the full analysis
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "Analysis Reasoning"}}]
                },
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": report.get("reasoning", "")}}]
                },
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "News Summary"}}]
                },
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": report.get("news_summary", "")}}]
                },
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "Raw Signal Data"}}]
                },
            },
            {
                "object": "block",
                "type": "code",
                "code": {
                    "language": "json",
                    "rich_text": [{"text": {"content": json.dumps(signal_data, indent=2)}}],
                },
            },
        ],
    }

    try:
        resp = requests.post(
            "https://api.notion.com/v1/pages",
            headers={
                "Authorization":  f"Bearer {NOTION_API_KEY}",
                "Content-Type":   "application/json",
                "Notion-Version": "2022-06-28",
            },
            json=payload,
            timeout=15,
        )
        resp.raise_for_status()
        log.info("Notion page created for %s (%s)", ticker, action)
        return True
    except Exception as exc:
        log.error("Notion log error for %s: %s", ticker, exc)
        return False


# ──────────────────────────────────────────────────────────────────────────────
# Core pipeline — ties all three steps together
# ──────────────────────────────────────────────────────────────────────────────
def run_pipeline(ticker: str, signal_data: dict) -> dict:
    """Fetch news → analyze with Claude → log to Notion. Returns the report."""
    log.info("Pipeline start: %s", ticker)

    news   = fetch_news(ticker)
    log.info("  News fetched: %d articles", len(news))

    report = analyze_with_claude(ticker, signal_data, news)
    log.info("  Claude: action=%s  confidence=%s", report.get("action"), report.get("confidence"))

    ok = log_to_notion(report, signal_data)
    log.info("  Notion log: %s", "OK" if ok else "FAILED")

    return report


# ──────────────────────────────────────────────────────────────────────────────
# Webhook endpoint — receives TradingView alerts
# ──────────────────────────────────────────────────────────────────────────────
@app.route("/webhook", methods=["POST"])
def webhook():
    """
    TradingView alert URL: http://<your-server>:5000/webhook

    Configure your TradingView alert message body as JSON, for example:
    {
      "ticker":    "{{ticker}}",
      "signal":    "BUY",
      "price":     {{close}},
      "timeframe": "{{interval}}",
      "strategy":  "My Strategy"
    }
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    ticker = data.get("ticker")
    if not ticker:
        return jsonify({"error": "Missing 'ticker' field"}), 400

    log.info("Webhook received: ticker=%s  signal=%s", ticker, data.get("signal"))

    # Run the pipeline in a background thread so the webhook returns immediately
    threading.Thread(target=run_pipeline, args=(ticker, data), daemon=True).start()

    return jsonify({"status": "processing", "ticker": ticker}), 202


@app.route("/health", methods=["GET"])
def health():
    """Quick health check."""
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat()}), 200


# ──────────────────────────────────────────────────────────────────────────────
# Monday 8 AM scheduled job
# ──────────────────────────────────────────────────────────────────────────────
def monday_watchlist_job():
    """Analyze every ticker in WATCHLIST — runs automatically each Monday at 08:00."""
    log.info("Monday 8 AM job started — analysing %d tickers", len(WATCHLIST))
    for ticker in WATCHLIST:
        signal_data = {
            "ticker":    ticker,
            "signal":    "SCHEDULED_REVIEW",
            "timeframe": "1W",
            "source":    "monday_cron",
        }
        run_pipeline(ticker, signal_data)
        time.sleep(3)   # brief pause between tickers to respect API rate limits
    log.info("Monday 8 AM job complete")


def run_scheduler():
    """Background thread that checks and fires scheduled jobs every minute."""
    schedule.every().monday.at("08:00").do(monday_watchlist_job)
    log.info("Scheduler running — Monday 08:00 job registered")
    while True:
        schedule.run_pending()
        time.sleep(60)


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Start the scheduler in a background daemon thread
    threading.Thread(target=run_scheduler, daemon=True).start()

    log.info("Trading Intelligence Agent starting on port %d", WEBHOOK_PORT)
    log.info("TradingView webhook URL  →  http://<your-server-ip>:%d/webhook", WEBHOOK_PORT)
    log.info("Health check             →  http://<your-server-ip>:%d/health", WEBHOOK_PORT)

    # Use debug=False in production; the Flask dev server is fine for personal use
    app.run(host=WEBHOOK_HOST, port=WEBHOOK_PORT, debug=False)


# ──────────────────────────────────────────────────────────────────────────────
# System cron alternative (if you prefer OS-level scheduling over the built-in
# schedule library, add this line to your crontab with: crontab -e)
#
#   0 8 * * 1  cd /path/to/project && python trading_agent.py
#
# To trigger just the Monday job without starting the server:
#   python -c "from trading_agent import monday_watchlist_job; monday_watchlist_job()"
# ──────────────────────────────────────────────────────────────────────────────
