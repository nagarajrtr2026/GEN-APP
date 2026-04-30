# Genora AI Backend

AI-powered backend service that converts plain-English prompts into structured software architecture outputs such as UI schema, API schema, database schema, authentication roles, and business logic.

---

##  Overview

Genora AI Backend is built with **FastAPI** and designed as a modular AI pipeline.

It accepts prompts like:

* Build hospital app with doctors and appointments
* Create ecommerce platform with products and orders
* Build school management app with attendance

Then returns structured JSON architecture.

---

##  Features

* Natural language prompt processing
* Intent extraction pipeline
* System design generation
* UI schema generation
* API endpoint generation
* Database schema generation
* Auth roles & permissions
* Business logic generation
* Validation engine
* Auto repair engine
* Metrics tracking
* History storage
* Swagger API docs

---

##  Tech Stack

* Python 3.11+
* FastAPI
* Uvicorn
* Pydantic
* SQLite / PostgreSQL (optional)
* Groq / Gemini / OpenAI provider support
* REST API

---

##  Project Structure

```text
backend/
│── app/
│   ├── main.py
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── api/routes/
│   ├── services/
│   ├── utils/
│   └── tests/
│
│── requirements.txt
│── .env.example
│── README.md
│── run.py
```

---

##  Installation

### 1. Clone Repo

```bash
git clone <repo-url>
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac / Linux

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

##  Environment Variables

Create `.env`

```env
AI_PROVIDER=groq
API_KEY=api_key
```

Supported providers:

* groq
* gemini
* openai
* dummy

---

##  Run Server

```bash
python run.py
```

or

```bash
uvicorn app.main:app --reload
```

Server runs at:

```text
https://gen-app-u1l1.onrender.com
```

Swagger Docs:

https://gen-app-u1l1.onrender.com/docs
```

---

## API Endpoints

### Health Check

```http
GET /api/v1/health
```

### Generate Architecture

```http
POST /api/v1/generate
```

Request:

```json
{
  "prompt": "Build hospital app with doctors and appointments"
}
```

### Metrics

```http
GET /api/v1/metrics
```

### History

```http
GET /api/v1/history
```

---

##  Example Response

```json
{
  "success": true,
  "data": {
    "app_name": "Hospital Management",
    "ui": {},
    "api": {},
    "database": {},
    "auth": {}
  }
}
```

---

##  Pipeline Flow

```text
Prompt
→ Intent Extractor
→ System Designer
→ Schema Generator
→ Validator
→ Repair Engine
→ Final JSON Output
```

---

## Testing

```bash
pytest
```

---

##  Deployment

Recommended:

* Backend: Render 
* Frontend: Vercel 

---

##  Notes

* Use `.env` for API keys
* Never commit secrets
* Enable CORS for frontend deployment
* Free AI providers may have quota limits

---

## 👨‍💻 Author

Genora AI Project

---
