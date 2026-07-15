# TextLyra — One-Person Business Playbook

**The business:** AI agents on WhatsApp & SMS for local businesses — answering customers,
booking appointments, and rescuing missed calls, 24/7.

**The goal:** $20,000/month recurring within 6 months, run by one person.

---

## 1. The math to $20k/month

| Plan | Price | Clients needed for $20k |
|---|---|---|
| Starter | $149/mo | 134 (too many — avoid anchoring here) |
| Growth | $299/mo | **67** |
| Mix (realistic) | ~$260 avg | ~77 |

**Target: 67 Growth clients in 26 weeks ≈ 2.5 new clients/week.**
With a 30% close rate on demos, that's ~8 demos/week, from ~40 outreach conversations/week.
Entirely doable for one person because *fulfillment is automated* (see §4).

Milestones:
- Month 1: 5 clients ($1.5k MRR) — founding members, white-glove, collect testimonials
- Month 2: 12 clients ($3.6k)
- Month 3: 22 clients ($6.6k) — first case studies published, referrals kick in
- Month 4: 35 clients ($10.5k)
- Month 5: 50 clients ($15k)
- Month 6: 67 clients ($20k) ✅

Churn assumption: <5%/mo if the agent demonstrably books revenue (weekly report is the retention weapon).

## 2. Brand & domain

- **Name:** TextLyra
- **Domain:** register **textlyra.com** on GoDaddy (verified zero web presence as of Jul 2026;
  do the final 10-second availability check in GoDaddy's search bar before buying).
- Backups if it's gone by the time you buy: **replyotter.com**, **textlyra.ai**, **trytextlyra.com**.
- Buy the .com only. Skip the upsells (privacy is usually free now; no need for 10 TLDs).

## 3. Launch checklist (week 1)

1. Register textlyra.com (~$12/yr).
2. Deploy `index.html` — fastest paths:
   - **GitHub Pages:** repo Settings → Pages → serve from branch (free), point GoDaddy DNS at it, or
   - **Netlify/Vercel free tier:** drag-and-drop deploy, add custom domain.
3. Submit the waitlist form once yourself → confirm the FormSubmit activation email
   that arrives at yerianmainrai@gmail.com (one-time; after that all signups land in your inbox).
4. Set up `hello@textlyra.com` (Zoho Mail free tier, or Google Workspace $6/mo).
5. Create Google Business Profile + Instagram/Facebook page (social proof surface, ~1 hr).

## 4. The self-running fulfillment stack

The product itself is assembled from automation platforms — you configure, you don't code from scratch:

| Layer | Tool | Cost |
|---|---|---|
| WhatsApp Business API | 360dialog / Twilio / Meta Cloud API | ~free–$50/mo |
| SMS | Twilio | ~$1/number + usage (bill into plan) |
| AI agent brain | Claude API (claude-sonnet-5 — best cost/quality for support agents) | ~$3–10/client/mo |
| Orchestration | n8n (self-hosted, free) or Make.com | $0–29/mo |
| Calendar booking | Cal.com API / client's existing Calendly/Fresha | free |
| Client dashboard/report | Automated weekly email (n8n) | $0 |
| Billing | Stripe subscriptions + automatic dunning | 2.9% |

**Total COGS: roughly $15–25/client/mo → ~92% gross margin at $299.**

One-person rules:
- **One onboarding form, one template.** Every client fills the same intake form; a templated
  n8n workflow + prompt pack gets cloned per client. Setup time per client: target <2 hrs by month 2.
- **Weekly report is automated.** "Your agent handled 214 conversations and booked 31 appointments
  worth ~$2,300" — this email renews the subscription for you.
- **Human handoff goes to the CLIENT, not you.** You are not in the message loop; escalations
  route to the business owner's phone.
- **Support window:** async only (email/WhatsApp), 24h SLA. No phone support below $299.

## 5. Customer acquisition (the only manual job)

Time budget: ~15 hrs/week on sales, everything else automated.

1. **Missed-call demo (highest converting):** call 20 local businesses at lunch/rush hour.
   The ones who don't answer just proved they need you. Walk in / email with:
   "I called Tuesday at 1pm — no answer. Here's what a customer sees instead with TextLyra…" + live demo number.
2. **Live demo number:** a WhatsApp number running a TextLyra agent for a fictional salon.
   Prospects text it and sell themselves. Put it on the landing page later.
3. **One niche per month.** Month 1: salons. Month 2: dentists. Templates compound —
   the 10th salon takes 30 minutes to onboard.
4. **Referral engine:** one month free per referral that converts (costs you ~$20, earns $299/mo).
5. **Local Facebook groups + Google Maps scraping** for outreach lists (n8n can automate list building).

## 6. What NOT to do

- Don't build custom features per client — sell the template or walk away.
- Don't offer one-off setups; recurring only (setup fee optional: $199, waived for founding members).
- Don't chase enterprise. 67 small businesses at $299 beat one enterprise deal you can't service alone.
- Don't hire before $15k MRR — automate or decline.

## 7. Files in this folder

- `index.html` — the landing page (self-contained, working waitlist form). Deploy as-is.
- `PLAYBOOK.md` — this file.
