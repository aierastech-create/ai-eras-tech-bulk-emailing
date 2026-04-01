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
    B --> C[TemplateEngine (Jinja2)]
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

<style>#mermaid-1775063279671{font-family:sans-serif;font-size:16px;fill:#333;}#mermaid-1775063279671 .error-icon{fill:#552222;}#mermaid-1775063279671 .error-text{fill:#552222;stroke:#552222;}#mermaid-1775063279671 .edge-thickness-normal{stroke-width:2px;}#mermaid-1775063279671 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1775063279671 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1775063279671 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1775063279671 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1775063279671 .marker{fill:#333333;}#mermaid-1775063279671 .marker.cross{stroke:#333333;}#mermaid-1775063279671 svg{font-family:sans-serif;font-size:16px;}#mermaid-1775063279671 .label{font-family:sans-serif;color:#333;}#mermaid-1775063279671 .label text{fill:#333;}#mermaid-1775063279671 .node rect,#mermaid-1775063279671 .node circle,#mermaid-1775063279671 .node ellipse,#mermaid-1775063279671 .node polygon,#mermaid-1775063279671 .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#mermaid-1775063279671 .node .label{text-align:center;}#mermaid-1775063279671 .node.clickable{cursor:pointer;}#mermaid-1775063279671 .arrowheadPath{fill:#333333;}#mermaid-1775063279671 .edgePath .path{stroke:#333333;stroke-width:1.5px;}#mermaid-1775063279671 .flowchart-link{stroke:#333333;fill:none;}#mermaid-1775063279671 .edgeLabel{background-color:#e8e8e8;text-align:center;}#mermaid-1775063279671 .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#mermaid-1775063279671 .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#mermaid-1775063279671 .cluster text{fill:#333;}#mermaid-1775063279671 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:sans-serif;font-size:12px;background:hsl(80,100%,96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#mermaid-1775063279671:root{--mermaid-font-family:sans-serif;}#mermaid-1775063279671:root{--mermaid-alt-font-family:sans-serif;}#mermaid-1775063279671 flowchart-v2{fill:apa;}</style>
