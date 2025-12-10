# AI-Legal-Assistant-For-Property-Transactions-
> **Democratizing legal access.** This project uses a hybrid AI approach to analyze Indian Property Sale Deeds, flagging risks and translating legal jargon into simple English for buyers and legal professionals.

---

## 🧐 Problem Statement
Buying property involves signing complex **Sale Deeds** filled with archaic legal terminology. Laypeople often miss critical red flags like:
* Missing **Indemnity Clauses** (protection against future claims).
* Vague **Possession Dates**.
* Lack of **Dispute Resolution** mechanisms.

**AI Legal Assistant for property transactions** acts as a first-line automated auditor to verify document hygiene and highlight risks before you sign.

---

## 🚀 Key Features

### 1. 🧠 Hybrid Analysis Engine
Combines two powerful methods for maximum accuracy:
* **Deterministic Rule Engine:** Uses Regex and heuristics to instantly flag "High Severity" issues (e.g., missing possession date, absence of arbitration clause).
* **LLM (Google Gemini):** Performs semantic analysis to understand the *context* of clauses, summarize the deal, and explain terms in plain English.

### 2. 📑 Document Summarization
Automatically extracts key details:
* **Parties:** Buyer & Seller identities.
* **Property:** Address, Survey Numbers, Area.
* **Financials:** Total consideration, payment methods, and schedules.

### 3. ⚖️ Clause Explainer
No more confusing legalese. The AI breaks down every section:
* **Legal Summary:** Technical explanation for lawyers.
* **Simple English:** A 5th-grade reading level translation for buyers (e.g., *"This clause means if someone claims the land belongs to them later, the seller has to pay you back."*).

### 4. 🚩 Fraud & Risk Detection
Categorizes the document as **Normal**, **Suspicious**, or **High Risk** based on:
* Missing mandatory clauses (Indemnity, Jurisdiction).
* Suspicious phrasing ("Seller shall not be responsible...").
* Lack of witness sections or boundary definitions.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit (Interactive Web UI)
* **LLM Core:** Google Gemini Flash (Generative AI)
* **PDF Processing:** pdfplumber & PyPDF2
* **Data Manipulation:** Pandas & NumPy
* **Rule Engine:** Python Regex & Custom Heuristics

---

## 📂 Project Structure

```bash
├── data_extraction_for_ai_legal_assisstant.ipynb   # Extraction logic
├── AI_Legal_Assistant.ipynb                        # Core analysis logic
├── app.py                                          # Streamlit Dashboard
├── sale_deeds/                                     # Input Data (60 Documents)
│   ├── non_fraud/                                  # 50 Normal Sale Deeds
│   └── fraud/                                      # 10 Fraud/Risky Sale Deeds
└── README.md                                       # Documentation
