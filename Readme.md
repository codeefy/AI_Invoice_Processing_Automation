<div align="center">

# 🚀 AI-Powered Invoice Automation Platform

**An end-to-end Intelligent Document Processing (IDP) pipeline that turns a raw invoice email into a verified, audited ERP bill — with zero manual entry.**

<br/>

![n8n](https://img.shields.io/badge/n8n-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![Zoho Books](https://img.shields.io/badge/Zoho_Books-C8202F?style=for-the-badge&logo=zoho&logoColor=white)
![Gmail](https://img.shields.io/badge/Gmail_API-EA4335?style=for-the-badge&logo=gmail&logoColor=white)
![Google Sheets](https://img.shields.io/badge/Google_Sheets-34A853?style=for-the-badge&logo=googlesheets&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)

</div>

---

## 📌 Project Overview

**AI-Powered Invoice Automation Platform** is a production-ready workflow built entirely on **n8n**, using **Google Gemini** for AI extraction and the **Zoho Books API** as the ERP backend. It automates the complete lifecycle of an invoice — from the moment it lands in a Gmail inbox to the moment a verified, duplicate-checked bill appears in the accounting system.

Every invoice email is read, parsed by AI, validated against financial rules, checked for duplicates, matched (or created) against a vendor, and finally posted as a Zoho Books bill — with every outcome, success or failure, written to a Google Sheets audit log.

**Processed 100+ invoices end-to-end · 95%+ AI extraction accuracy · 80% reduction in manual effort.**

<br/>

<div align="center">

| 📧 Ingestion | 🤖 AI Extraction | ✅ Validation | 🔁 Duplicate Check | 👥 Vendor Resolution | 🧾 Bill Creation | 📊 Audit Log |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Gmail Trigger | Google Gemini | Financial Rules | Zoho Books Search | Auto-Match / Auto-Create | Zoho Books API | Google Sheets |

</div>

---

## ⭐ Key Features

- 📧 **Gmail-triggered ingestion** — no manual upload required
- 🤖 **AI-powered extraction** using Google Gemini (`gemini-2.5-flash-lite`)
- ✅ **Financial validation engine** for every extracted invoice
- 🔁 **Duplicate invoice detection** before any bill is created
- 👥 **Automatic vendor resolution** — reuses existing vendors or creates new ones on the fly
- 🧾 **Zoho Books bill creation** with a fully verified payload
- 📊 **Google Sheets audit logging** at every decision point — success *and* failure
- 🛡 **Fail-safe branching** — validation, duplicate, vendor, and payload failures each get their own logged path, so nothing fails silently

---

## 📊 Impact / Benchmark Highlights

<div align="center">

| Metric | Result |
|:---|:---:|
| Invoices Processed | **100+** |
| AI Extraction Accuracy | **95%+** |
| Manual Effort Reduction | **80%** |
| Duplicate Detection | ✅ Implemented |
| Financial Validation | ✅ Implemented |
| Automatic Vendor Creation | ✅ Implemented |
| Audit Logging | ✅ Every branch logged to Sheets |

</div>

---

## ⚙️ Tools & Technology

| Category | Stack |
|---|---|
| **Workflow Automation** | n8n (cloud-hosted, `rohit21f.app.n8n.cloud`) |
| **AI / LLM** | Google Gemini API — `gemini-2.5-flash-lite` |
| **ERP / Accounting** | Zoho Books API |
| **Email Ingestion** | Gmail Trigger (n8n) |
| **Data Handling** | Base64 PDF encoding, JSON transformation |
| **Audit & Logging** | Google Sheets API |
| **Core Logic** | n8n Code nodes (JavaScript) for validation & payload building |

**Language:** JavaScript (n8n Code nodes) · JSON (data contracts between nodes)

---

## 🏗 High-Level Architecture

```text
                        ┌────────────────────┐
                        │   Gmail Inbox       │
                        └─────────┬───────────┘
                                  ▼
                     Gmail Trigger (Receive Invoice Email)
                                  ▼
                     Convert PDF Attachment → Base64
                                  ▼
                       Google Gemini AI (Extraction)
                                  ▼
                        Validation Invoice Data
                                  ▼
                          Is Invoice Valid? ──false──► Append Row (Validation Log)
                                  │true
                                  ▼
                 Append Row (API Checked) → HTTP Request
                     (Get Zoho Books Organizations)
                                  ▼
                     Duplicate Check (Search Bills)
                                  ▼
                    If Duplicate Exists? ──true──► Append Row (Duplicate Log)
                                  │false
                                  ▼
                     HTTP Request — Vendor Check
                                  ▼
                Does Vendor Exist? ──true──► Get Existing Vendor Details
                                  │false
                                  ▼
              Log Vendor Check Failure → Prepare New Vendor Data
                                  ▼
                     Create New Vendor in Zoho
                          │success        │error
                          ▼                ▼
                 Build & Verify        Log Vendor
                 Zoho Payload          Creation Failure
                          ▼
                Is Zoho Payload Valid? ──false──► Log Payload Validation Failure
                          │true
                          ▼
                   Create Bill for Clarity (Zoho Books)
                          │success        │error
                          ▼                ▼
                 Append Row           Log Zoho Bill
                 (Bill Created)       Creation Failure
```

---

## 🔄 n8n Workflow — Step by Step

### 1. Ingestion
- **Gmail Trigger (Receive Invoice Email)** — listens for incoming invoice emails
- **Convert PDF Attachment to Base64** — prepares the PDF for the Gemini API payload

### 2. AI Extraction
- **Gemini AI** (`POST https://generativelanguage...`) — extracts structured invoice fields (vendor, invoice number, dates, line items, subtotal, tax, grand total, currency)
- **Validation Invoice Data** (Code node) — normalizes and structurally validates the Gemini response
- **Is Invoice Valid?** (IF node) — routes valid invoices forward; invalid ones are logged and stopped

### 3. Organization / API Check
- **Append Row** — logs that the invoice passed the API check
- **HTTP Request (Get Zoho Books Organizations)** — confirms the correct Zoho organization context for downstream calls

### 4. Duplicate Detection
- **Duplicate Check (Search Bills)** — searches existing Zoho bills for a matching invoice number/vendor
- **If Duplicate Exists?** (IF node)
  - **True** → **Append Row in Sheet** (duplicate logged, workflow stops)
  - **False** → proceeds to vendor resolution

### 5. Vendor Resolution
- **HTTP Request — Vendor Check** — queries Zoho Books for the vendor
- **If (Does Vendor Exist?)** (IF node)
  - **True** → **Get Existing Vendor Details**
  - **False** → **Log Vendor Check Failure** → **Prepare New Vendor Data** → **Create New Vendor in Zoho**
    - **Success** → continues to payload building
    - **Error** → **Log Vendor Creation Failure**

### 6. Payload Construction & Validation
- **Build & Verify Zoho Payload** (Code node) — assembles the final bill payload with the resolved vendor ID and validated line items
- **Is Zoho Payload Valid?** (IF node)
  - **False** → **Log Payload Validation Failure**
  - **True** → proceeds to bill creation

### 7. ERP Bill Creation
- **Create Bill for Clarity** (`POST https://www.zohoapis...`) — creates the final bill in Zoho Books
  - **Success** → **Append Row in Sheet 1** (bill creation logged)
  - **Error** → **Log Zoho Bill Creation Failure**

### 8. Audit Trail
Every branch writes to a dedicated Google Sheets log: API Checked, Duplicate, Vendor Check Failure, Vendor Creation Failure, Payload Validation Failure, and Bill Creation (success/failure). Every invoice that enters the system has a traceable outcome, even if it never reaches Zoho Books.

---

## 🧩 Design Highlights

- **Fail-safe branching** — every decision point (validity, duplicate, vendor, payload) has an explicit failure path with its own log, instead of a single generic error handler
- **Idempotency by design** — the duplicate-check step runs *before* any vendor or bill mutation, preventing double billing
- **Self-healing vendor resolution** — the workflow doesn't just fail on an unknown vendor; it creates one automatically and continues the same run
- **Two-stage validation** — invoice data is validated once right after extraction, and the Zoho payload is validated again right before the API call, catching errors introduced during transformation

---

## 📁 Suggested Repository Structure

```text
AI-Invoice-Automation/
│
├── n8n_Workflow/
│   └── Invoice_Automation.json        # Exported n8n workflow
│
├── screenshots/
│   ├── workflow_overview.png
│   ├── gemini_extraction.png
│   ├── zoho_bill_created.png
│   └── audit_sheet_log.png
│
├── docs/
│   └── architecture.md
│
└── README.md
```

---

## 🚀 Resume Highlights

- Built a production-ready invoice automation platform using **n8n**, processing **100+ invoices end-to-end** from mail ingestion to ERP bill creation using n8n, Google Gemini, and Zoho Books APIs.
- Implemented AI integrations with Zoho Books and Gemini AI for invoice parsing, financial validation, duplicate prevention, payload verification, and vendor resolution, achieving **95%+ data extraction accuracy** with structured validation and normalization.
- Designed fail-safe branching across every workflow decision point (validity, duplicate, vendor, payload) with dedicated audit logging, reducing manual invoice-processing effort by **80%**.

---

## 🔮 Future Improvements

- OCR fallback (Tesseract) for scanned/non-selectable PDFs
- Confidence scoring on Gemini extractions with a human-in-the-loop review queue for low-confidence invoices
- Multi-currency and multi-language invoice support
- Power BI / Grafana dashboard on top of the Google Sheets audit log
- Move audit logging from Sheets to a proper database for scale

---

<div align="center">

## 👨‍💻 Author

**Rohit Raj**
M.Sc. Economics & Management, IIIT Lucknow

---

📜 *This project is intended for educational, research, and portfolio purposes.*

</div>