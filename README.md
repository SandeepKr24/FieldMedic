# 🩺 FieldMedic

**FieldMedic** is an AI-powered clinical decision support system designed to assist frontline healthcare workers by providing evidence-backed patient triage recommendations.

The system combines Retrieval-Augmented Generation (RAG), semantic search, clinical safety rules, and a Large Language Model to produce structured triage decisions.

---

## Features

- AI-powered patient triage
- Retrieval-Augmented Generation (RAG)
- Semantic search using Sentence Transformers
- PostgreSQL + pgvector vector database
- FastAPI backend
- Streamlit frontend
- Rule-based clinical safety layer
- Structured JSON outputs
- Knowledge ingestion pipeline
- Evaluation harness for testing

---

## System Architecture

```
                Streamlit UI
                      │
                      ▼
               FastAPI Backend
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
 Retrieval Pipeline          Safety Rules
        │                           │
        └─────────────┬─────────────┘
                      ▼
              Gemini LLM Reasoner
                      │
                      ▼
            Structured Triage Output
                      ▲
                      │
       PostgreSQL + pgvector Knowledge Base
```

---

## Tech Stack

- Python
- FastAPI
- Streamlit
- PostgreSQL
- pgvector
- Docker
- Sentence Transformers
- Google Gemini API

---

## Project Structure

```
FieldMedic/
│
├── src/
│   ├── agents/
│   ├── prompts/
│   ├── infra/
│   ├── eval/
│   └── app.py
│
├── ui/
│   └── Home.py
│
├── init/
│
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/FieldMedic.git
cd FieldMedic
```

Create a virtual environment

```bash
python -m venv .venv
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example`.

---

## Running with Docker

```bash
docker compose up --build
```

---

## Services

FastAPI

```
http://localhost:3000/docs
```

Streamlit

```
http://localhost:8501
```

---

## API Endpoints

### POST `/triage`

Accepts patient symptoms and vitals and returns a structured triage recommendation.

### POST `/knowledge`

Adds medical knowledge to the vector database.

### GET `/status`

Health check endpoint.

---

## Example Response

```json
{
    "triage": "Urgent",
    "care_plan": "Immediate physician assessment and hydration.",
    "icd10": [
        "J18.9"
    ],
    "summary": "Patient presents with fever and productive cough. Evidence suggests possible community-acquired pneumonia.",
    "confidence": 0.92
}
```

---

## Future Improvements

- PDF knowledge ingestion
- Multi-provider LLM support
- Authentication
- Explainable AI citations
- Clinical audit logs
- Deployment on cloud infrastructure

---

## License

MIT License
