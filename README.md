# 🏠 AI Property Agent

An AI-powered real estate assistant that helps customers find properties through natural-language queries and automatically identifies high-intent leads.

The system combines **Generative AI, Hybrid RAG, ChromaDB, FastAPI, n8n, WhatsApp, and Google Sheets** to automate property search and lead management.

---

## 🚀 Features

* 🤖 Natural-language property search
* 🔎 Hybrid search using structured filters + semantic search
* 🧠 LLM-powered requirement extraction
* 📚 RAG with ChromaDB
* 💬 AI-generated property recommendations
* 🔥 Automatic HOT/WARM/COLD lead classification
* 📱 WhatsApp integration
* ⚙️ n8n workflow automation
* 📊 Automatic lead storage in Google Sheets
* 🛡️ Grounded responses to reduce hallucinations

---

## 💡 Business Problem

Real estate agents often spend significant time:

* Searching property listings manually
* Answering repetitive customer questions
* Identifying serious buyers
* Recording customer information
* Following up with leads

This project automates these tasks through an AI-powered workflow.

---

## 🏗️ Architecture

```text
Customer
   ↓
WhatsApp
   ↓
n8n
   ↓
Lead Analysis
   ↓
┌───────────────────────┐
│                       │
▼                       ▼
HOT Lead             Property Query
│                       │
▼                       ▼
Google Sheets       FastAPI
                        ↓
                 Requirement Extraction
                        ↓
                  Hybrid Search
                    ↙       ↘
             Structured    ChromaDB
               Search      Semantic Search
                    ↘       ↙
                        ↓
                    AI Response
                        ↓
                     WhatsApp
```

---

## 🧠 Hybrid RAG

The system combines two types of search.

### Structured Search

Used for exact requirements:

```text
City
Price
Size
Bedrooms
Bathrooms
Property Type
```

### Semantic Search

Used for natural-language preferences such as:

```text
modern
peaceful
family-friendly
near commercial facilities
```

Property data is converted into embeddings using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

and stored in **ChromaDB**.

---

## 🔄 AI Pipeline

### Property Search

```text
User Query
    ↓
Requirement Extraction
    ↓
Structured + Semantic Search
    ↓
Relevant Properties
    ↓
Grounded LLM Response
```

### Lead Qualification

```text
Customer Message
    ↓
Lead Analysis
    ↓
HOT / WARM / COLD
    ↓
Google Sheets
```

Example HOT lead:

```text
I like the 5 Marla house in B-17.
I want to buy it and visit tomorrow.
```

The system extracts:

```json
{
  "intent": "visit_request",
  "lead_status": "HOT",
  "visit_requested": true,
  "name": "Ali Khan",
  "phone": "03001234567",
  "property_query": "5 Marla house in B-17, Islamabad"
}
```

---

## 🛠️ Tech Stack

| Technology            | Purpose                     |
| --------------------- | --------------------------- |
| Python                | Backend & AI logic          |
| Groq                  | LLM inference               |
| Sentence Transformers | Embeddings                  |
| ChromaDB              | Vector database             |
| Pandas                | Data processing & filtering |
| FastAPI               | REST API                    |
| n8n                   | Workflow automation         |
| WhatsApp / GREEN-API  | Customer communication      |
| Google Sheets         | Lead management             |

---

## 📁 Project Structure

```text
AI-Property-Agent/
│
├── app/
│   ├── preprocess.py
│   ├── search.py
│   ├── rag.py
│   ├── extractor.py
│   ├── hybrid_search.py
│   ├── agent.py
│   ├── lead.py
│   └── main.py
│
├── data/
│   ├── properties.csv
│   └── properties_clean.csv
│
├── chroma_db/
├── n8n/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd AI-Property-Agent
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

Activate on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env`:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 🗄️ Setup

### Clean the dataset

```bash
python -m app.preprocess
```

### Build the vector database

```bash
python -m app.rag
```

### Test the property agent

```bash
python -m app.agent
```

---

## 🚀 Run the API

```bash
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Available endpoints

```text
GET  /
POST /property-search
POST /lead-analysis
```

---

## 💬 Example

### Customer

```text
I want a 5 marla house in Islamabad under 2 crore
with at least 4 bedrooms.
```

### AI

```text
🏠 Here are the properties matching your requirements:

1. Islamabad Highway, Islamabad
📐 Size: 5 Marla
🛏️ Bedrooms: 5
🛁 Bathrooms: 6
💰 Price: PKR 19,000,000

2. Bani Gala, Islamabad
📐 Size: 5 Marla
🛏️ Bedrooms: 4
🛁 Bathrooms: 4
💰 Price: PKR 19,000,000

Would you like more details or would you like
to schedule a visit?
```

---

## 🛡️ Grounded AI

The AI is instructed to recommend **only properties retrieved from the available dataset**.

It does not invent:

* Property listings
* Prices
* Locations
* Property sizes
* Bedrooms
* Bathrooms
* Unsupported facilities or features

This helps reduce hallucinations and keeps recommendations grounded in available data.

---

## 📊 Business Value

The system helps real estate businesses:

* Reduce repetitive manual work
* Respond to customers faster
* Automatically search property listings
* Identify serious buyers
* Capture leads automatically
* Organize customer information
* Automate follow-ups through n8n

---

## 🔮 Future Improvements

* Live property database/API
* Appointment scheduling
* Automated lead follow-ups
* CRM integration
* Urdu/Roman Urdu support
* Voice-based property search
* Property image analysis
* Multi-agent architecture

---

## 👩‍💻 Author

**Kashaf Fayyaz**
B.S. Artificial Intelligence — COMSATS University Islamabad

---

## 📌 Project Summary

**AI Property Agent** transforms a simple property inquiry into an automated business workflow:

```text
Customer
   ↓
WhatsApp
   ↓
AI Understanding
   ↓
Hybrid Property Search
   ↓
AI Recommendation
   ↓
Lead Qualification
   ↓
Google Sheets
   ↓
Agent Follow-up
```

Built with **Python, Generative AI, RAG, ChromaDB, FastAPI, n8n, and WhatsApp automation**.
