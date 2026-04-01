# 📬 MailForge | Bulk Email Automation & Campaign Engine (Python v2.0)

**MailForge** is a professional-grade, modular **bulk email automation engine** designed to handle dynamic templating, attachments, and large-scale campaigns with **reliability, extensibility, and production-ready architecture**.

---

## 🏛️ Project History & Vision

- **v1.0 (Legacy)** – A simple Python script (2021) that sent dynamic templated emails from CSV files. Functional, but monolithic, insecure, and limited in scalability.
- **v2.0 (Current)** – Complete **rewrite with senior-level system design**:
  - Modular architecture with **core, services, providers, infra, and CLI layers**
  - Support for dynamic templating using **Jinja2**
  - Configurable **SMTP provider abstraction** with future API provider support (SendGrid, Mailgun)
  - Robust logging, retry logic, and rate-limiting
- **Vision**: Transform MailForge into a fully **extensible email campaign platform** capable of multi-channel outreach, scheduling, analytics, and integration with enterprise systems.

---

## 🎯 Scope & Features

### Core Features:

- ✅ **Dynamic Templating** – Markdown + Jinja2 templates with unlimited variables
- ✅ **CSV/JSON Data Ingestion** – Supports structured recipient data from multiple sources
- ✅ **Attachment Management** – Add multiple attachments per campaign
- ✅ **SMTP Provider Abstraction** – Currently supports SMTP; API integrations planned
- ✅ **Retry Logic & Rate Limiting** – Safe bulk sending without triggering spam detection
- ✅ **Logging & Reporting** – File + console logs for audit and success tracking
- ✅ **Command-Line Interface** – Flexible CLI to launch campaigns

### Senior-Level Architecture Highlights:

- Modular design: `core/`, `services/`, `providers/`, `infra/`, `cli/`
- Extensible provider layer for future integrations
- Centralized configuration via `.env` for security and flexibility
- Orchestration layer (`CampaignEngine`) separates parsing, templating, and delivery

---

## 🚀 Milestones

1. **2021** – v1.0 script: CSV → email templating (legacy)
2. **2026 Q1** – v2.0 rewrite with:
   - Modular architecture
   - SMTP abstraction
   - Retry and rate limiting
   - Logging & CLI interface
3. **Future** – v3.0:
   - API integrations (SendGrid/Mailgun)
   - Multi-channel outreach (SMS, WhatsApp)
   - Scheduling and campaign analytics
   - Web dashboard & REST API

---

## 🏗️ Architecture Flow (Mermaid)

```mermaid
flowchart TD
    A[CSV / JSON Data] --> B[CSVParser / Data Validation]
    B --> C[TemplateEngine Jinja2]
    C --> D[CampaignEngine Orchestration]
    D --> E[SMTPProvider / APIProvider]
    D --> F[AttachmentService]
    E --> G[Recipients Inbox]
    F --> E
    D --> H[Logging & Reporting]
```

**Legend** :

- `CampaignEngine` orchestrates data → templates → attachments → provider
- `Logging & Reporting` captures audit trail and errors
- Provider abstraction ensures extensibility

---

## 📂 Folder Structure

<pre class="overflow-visible! px-0!" data-start="3289" data-end="3798"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="w-full overflow-x-hidden overflow-y-auto pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>MailForge/</span><br/><span>├── core/                # CSV parser, template engine</span><br/><span>├── services/            # Campaign orchestration, attachment management</span><br/><span>├── providers/           # SMTP and future API providers</span><br/><span>├── infra/               # Configuration and logging</span><br/><span>├── cli/                 # Command-line interface</span><br/><span>├── templates/           # Markdown/Jinja2 templates</span><br/><span>├── data/                # Sample CSV / JSON data</span><br/><span>├── attachments/         # Campaign attachments</span><br/><span>├── README.md</span><br/><span>├── requirements.txt</span><br/><span>├── .env.example</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

## ⚙️ Usage

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Create `.env` file (use `.env.example` as reference):

```
DISPLAY_NAME=Your Name
SENDER_EMAIL=you@example.com
PASSWORD=your_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
RATE_LIMIT=1
RETRY_COUNT=3
```

3. Prepare CSV file (`data/recipients.csv`) with **EMAIL** column.
4. Prepare Markdown template (`templates/template.md`) with Jinja2 variables:

```
Hi {{ NAME }},

Your bill of Rs. {{ PRICE }} for {{ MONTHS }} is due.

Thank you,
{{ DISPLAY_NAME }}
```

5. Run campaign via CLI:

```
python cli/main.py --csv data/recipients.csv --template templates/template.md
```

---

## 📈 Current Status

- v2.0 fully modular
- SMTP provider functional
- CLI operational
- Logging, retry, and rate limiting implemented
- Future-ready for multi-provider, analytics, and scheduling

---

## 🔮 Future Upgrades

- ✅ Add SendGrid / Mailgun API provider
- ✅ Dry-run & preview modes
- ✅ Multi-channel messaging (SMS, WhatsApp)
- ✅ Campaign analytics and reporting dashboard
- ✅ Scheduling and queue management
- ✅ REST API & web interface

---

## 🏷️ Topics

bulk-email-automation
email-campaign-engine
python-email-automation
SMTP
Jinja2
markdown-email
CLI-tool
dynamic-templating
attachments
retry-logic
rate-limiting
logging
CSV-ingestion
extensible-architecture
modular-python
email-marketing
campaign-engine
portfolio-project
professional-python
MailForge

---
