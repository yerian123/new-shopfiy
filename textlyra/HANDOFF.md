# TextLyra — Project Handoff / Context Document

> Paste this into any new Claude Code session to continue the project. Last updated: 2026-07-16.

## 1. What this project is

**TextLyra** — a one-person business selling AI receptionists (WhatsApp + SMS + phone) to local
service businesses. Owner: Yerian (yerianmainrai@gmail.com), based in **Surrey, BC, Canada**,
selling across Metro Vancouver and remotely anywhere.

- **Goal:** $20,000/month recurring within 6 months (started mid-July 2026).
- **Path:** ~55–67 clients. 2–3 closes/week. Fulfillment ~92% margin, almost fully automated;
  owner's manual job is sales (~15 hrs/wk) plus commission-only callers.

## 2. Services & pricing (all CAD, founding-member = 50% off "for life")

| Service | Price | Notes |
|---|---|---|
| Starter (text agent, 1 channel) | $149/mo | De-emphasize; don't anchor here |
| **Growth (main offer)** | **$299/mo** | WhatsApp + SMS agent, missed-call text-back, booking, reviews, follow-ups |
| AI Voice Receptionist add-on | $1,000 setup + $199/mo | Retell AI/Vapi + Twilio; AI answers calls owner misses (conditional forwarding) |
| Business Website add-on | $500 setup + $25/mo | AI-built one-pager on Cloudflare Pages, agent embedded, max 2 edits/mo |
| "Total Front Desk" bundle | $1,500 setup + $449/mo | All of the above |

**Website upsell ladder (decided Jul 19):** client websites and the demo site do NOT include or
mention AI. Sell Website $500 + $25/mo first → upsell "+AI texting on your site" $150/mo at the
close (Yerian only — callers never pitch AI) → full Growth $299/mo → Voice $1,000 + $199/mo.
Website sales script v2 (AI-free): docs.google.com/document/d/1ZFsI1Ga119tIU3NgOFczsc8-W1FLyyJObmI4BZfPfQY
Demo site: `textlyra/demo-apex-plumbing.html` (fictional Apex Plumbing, fake number 604-555-0123,
no AI mentions) — deploy to own Cloudflare Pages project; callers text this link mid-call.

- Guarantee: if it doesn't book its own cost in 30 days → refund the month. Month-to-month.
- **Payments: Interac e-Transfer to textlyra@gmail.com (auto-deposit ON) + Wave invoices (free) for
  first ~10 clients, then Stripe.** First month + setup collected before building.
- Caller pay: $25 per demo that shows + $150 per close (friends/contractors, weekly e-transfer).

## 3. Key decisions already made (don't re-litigate)

1. **Name/brand:** TextLyra. Domain **textlyra.com NOT yet purchased** — verified zero web presence
   (Jul 2026), user must do final GoDaddy check + buy. Backup name: replyotter.com.
2. **Niche #1: HOME SERVICES** (plumbers, HVAC, electricians, garage doors) — chosen over
   dentists/clinics (HIPAA/compliance risk + gatekeeping receptionists) and salons. Dentists =
   Month 3 expansion. User also wants lead sheets for dental/clinics and salons/barbers anyway (see §7).
3. **Sales motion:** missed-call test → DM/email/walk-in → 20-min demo (prospect texts the live
   demo agent) → close with founding offer. Friends make cold calls, owner closes.
4. **Email:** business inbox = **textlyra@gmail.com**. Cold-email limit 15–20/day on new Gmail;
   move volume to Instantly.ai + hello@textlyra.com around week 3.
5. Facebook: join BC/Vancouver/Surrey business + trades + neighbourhood groups; value-first
   (no pitching week 1); "data post" strategy using real missed-call test numbers.

## 4. Everything built so far

### In this GitHub repo (`yerian123/new-shopfiy`, branch `claude/ai-agent-landing-page-unbqog`)
- `textlyra/index.html` — full landing page (dark theme, WhatsApp-green). Contains: hero with
  simulated WhatsApp chat, stats, how-it-works, features, industries, pricing (CAD) with Voice
  ($1,000+$199) and Website ($500+$25) add-on cards, FAQ (incl. Surrey service-area Q), OG/share
  meta tags, favicon (green T), **working waitlist form → FormSubmit AJAX → textlyra@gmail.com**.
- `docs/index.html` — identical copy for one-click GitHub Pages (Settings→Pages→this branch+/docs).
- `textlyra/PLAYBOOK.md` — original business playbook (some prices outdated vs this doc; this doc wins).
- Note: `veytra.py` etc. in repo root = a SEPARATE unrelated project. Ignore.

### Hosting (action needed)
- Currently live at `https://cold-term-b973.yerianmainrai.workers.dev/` (Cloudflare Workers).
- **User dislikes personal name in URL** → move to Cloudflare **Pages** project named `textlyra`
  → `textlyra.pages.dev` (Direct Upload). May be running an OLD version — redeploy latest
  index.html (check: green T favicon + gold Voice card + blue Website card = latest).
- **FormSubmit activation may still be pending:** submit form once on live site → click
  "Activate" email in textlyra@gmail.com inbox → signups then flow automatically.

### Google Docs (in yerianmainrai@gmail.com's Drive)
1. **"TextLyra — Business Plan, Outreach System & Client Signing Playbook"**
   docs.google.com/document/d/13SwwkkFKMmWM86eAadF0cKnYTv6uMUBhACNfhEhKq_Q
   (full plan, outreach scripts, demo call structure, objection handling, closing script, KPIs)
2. **"TextLyra — 7-Day Execution Plan (Home Services Launch)"**
   docs.google.com/document/d/1OMl40XxNmajax1_dkuRmG0fQoOVNIsRwjHYdGUo6VGw
   (day-by-day launch, caller hiring pack, voice-upsell economics, FB warm-up plan)
3. **"TextLyra — Build Guide & Sales Ops Pack"** ← the operating manual
   docs.google.com/document/d/1ZV3cln3l8jgoY4TxygTzAHoAKOQYktRM8sD5iGKObRY
   (step-by-step builds for ALL services incl. full "Apex Plumbing" demo persona prompt,
   n8n architecture, missed-call text-back setup, Retell voice guide, website assembly line,
   e-transfer/Wave flow, caller pack w/ scripts, FB groups + exact posts, lead-sorting matrix,
   10 extra acquisition channels, build order). NOTE: doc says website $49/mo — price since
   changed to **$25/mo**.

### Google Sheet
- **"TextLyra — Lead & Outreach Tracker"**
  docs.google.com/spreadsheets/d/1TwJYl7uOOK4sNx695R0E_QYbKokZnXMvIJ0DeQTKtH0
  Columns: Business, Niche, City, Owner, Phone, Email, Website, Rating, Reviews, Answered Call?,
  DM Sent, Email 1/2/3, Demo Booked, Demo Held, Closed, Caller, Notes. (+ add "Offer" column.)
  Currently only an example row — needs real leads.

### Gmail (drafts in yerianmainrai@gmail.com — user should forward to textlyra@gmail.com → save as Templates)
- [TEMPLATE — Email 1, Day 0] "Tried calling [Business] yesterday"
- [TEMPLATE — Email 2, Day 3] "the $4,200 voicemail"
- [TEMPLATE — Email 3, Day 7] "closing the loop"
- [TEMPLATE — After demo] "Your TextLyra setup — 2 quick steps"

## 5. Tech stack for the product (build guide §2 has full steps)

Twilio (numbers/SMS/voice webhooks) + Meta WhatsApp Business API (or 360dialog) + **n8n**
(orchestration) + **Claude API, model claude-sonnet-5** (agent brain; JSON replies with
action: none|book|escalate) + Cal.com/Google Calendar (booking) + Retell AI (voice add-on)
+ Cloudflare Pages (client websites) + Wave (invoices) + FormSubmit (waitlist).
COGS ≈ $15–25/client/mo text; +$30–60 voice.

## 6. Leads found so far (Surrey, BC — verified businesses, need enrichment)

**Home services — best targets (small crews, skip giants like Pioneer/Reliance/Home Depot):**
Plumbing: Guru Plumbing (guruplumbing.ca), Well Done Plumbing (welldoneplumbing.ca), Your Guy
Plumbing & Drainage (yourguydrainage.ca), Papa Plumbing (papaplumbing.ca), Gator Plumbing
(gatorplumbing.ca, 604-653-7309), Nagra Bros (nagrabros.ca), Lambert Plumbing (lambertplumbing.ca).
HVAC: Vanheat Services (vanheatservices.com, 4.9★/231), Greenway Mechanical
(greenwaymechanical.com), ComfortPro HVAC (comfortprohvac.ca), ThermaCool (thermacool.ca),
Rocky Point HVAC (rockypointhvac.com), CJ Heating, R.E. MacDonald (remacdonald.com).
Electrical: BPM Electric (bpmelectric.com), Intense Voltage (intensevoltage.com), The Surrey
Electrician (thesurreyelectrician.ca), Dan Wilcox Electric (danwilcoxelectric.com), Expert
Electric (expertelectric.ca), Final Flash, Puri Electric, Zantex, AZ Electrical.

**Dental/clinics (Month-3 niche; compliance-aware pitch):** Surrey Central Dental
(surreycentraldental.com), Dental Group at Central City, Dove Dental (dovedentalsurrey.com),
ProActive Dental Studio, Newton Dental Group (dentistinsurrey.ca), Smile Well Dental.

**Salons/barbers:** Tommy Gun's (Grandview Corners), Bladez & Fadez (bladezandfadez.ca, 400+ 5★),
Trendzone (trendzonebarbershop.com), King's Barbershop, MVP Modern Barbers, Vintage Barber,
The Cutting Den, Eddy's, Jamals, BigBoss Hair Salon, Eden Hair Salon, Haides Surrey.

**Facebook groups to join (verified):** Small Business Owners of B.C.
(facebook.com/groups/smallbusinessownersbc), Business Owners of British Columbia
(facebook.com/groups/britishcolumbiabusiness), Vancouver Entrepreneurs & Business Owners
(facebook.com/groups/340991843314173), Business Owners of Vancouver
(facebook.com/groups/businessownersofvancouver) + search: Surrey community groups, Langley
small business, Fraser Valley business, BC contractors, Punjabi business owners Surrey.

## 7. IN-PROGRESS / NEXT TASKS (updated)

1. **[DONE] Three lead Google Sheets created**, ~90 verified businesses with PRIMARY OFFER
   + pitch angle + upsell assigned per row (one sheet per caller):
   - Leads 1 HOME SERVICES: docs.google.com/spreadsheets/d/1_Kv-jK3S0PLOk1YtTF77GAPNR-5ELa-QwN25ec9DbeE
   - Leads 2 DENTAL & CLINICS: docs.google.com/spreadsheets/d/1wNNR9Q_0TpMTJA5U0-lsUVh_aR1ISKdsNCozP8d4ndM
   - Leads 3 SALONS & BARBERS: docs.google.com/spreadsheets/d/19KU8H9OoJdYFVf7mQaMTxmxLD4pM3DhpOLOHhHmVdYI
   User scales each to hundreds with a Chrome Maps-scraper extension (same columns).
2. **[DONE] Caller Playbooks doc** (3 personalized niche scripts + objections + booking flow):
   docs.google.com/document/d/1IRseO78q0oAZW-eLyMkTStRWQumOmiQUi_kOmfyYW8k
   Placeholders to fill before callers start: [DEMO NUMBER] + Yerian's Calendly link.
3. **[DONE] Website restructured multi-page**: `textlyra/index.html` (compact home),
   `services.html`, `pricing.html` — synced to `docs/`. User must upload all 3 files
   to hosting together.
4. **[NOT DONE] Move hosting** off `cold-term-b973.yerianmainrai.workers.dev` (user dislikes
   name in URL) → Cloudflare Pages project "textlyra" → textlyra.pages.dev + FormSubmit
   activation via textlyra@gmail.com.
5. **[NOT DONE] Demo agent build** (Build Guide §2.0–2.2) — the critical path. Callers
   cannot start until the demo number works.
4. User checklist (human-only): buy textlyra.com; FormSubmit activation; Interac auto-deposit;
   Wave account; FB group join requests; forward Gmail templates; Twilio/Anthropic/n8n accounts;
   build demo agent (Build Guide §2.0–2.2, "Apex Plumbing" prompt); Calendly demo slots;
   hand Caller Pack to friends; Chrome-extension scrape to 150+ leads/niche.

## 8. Standing offers Claude made to the user

- Debug/build the n8n demo-agent flow and persona prompt together when user starts it.
- Sort + prioritize the lead sheets once populated.
- Write personalized first lines for the first 20 cold emails.

## 9. Session conventions

- Work on branch `claude/ai-agent-landing-page-unbqog`; keep `docs/index.html` in sync with
  `textlyra/` site files; commit + push after changes.
- All prices CAD. Honesty rule: no invented case-study numbers in outreach until real client
  results exist (Month 2+); demo-driven pitches until then.
