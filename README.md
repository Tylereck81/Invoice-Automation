# AI Invoice Automation

A small project exploring how AI can be integrated into an existing business workflow.

The goal is to automate invoice data extraction while keeping the existing backend responsible for validation, business rules, and storage.

## Architecture

### Current Workflow

    User
     ↓
    FastAPI
     ↓
    Pydantic Validation
     ↓
    SQLAlchemy
     ↓
    PostgreSQL

### AI-Powered Workflow

    Invoice (PDF/Text)
           ↓
          LLM
           ↓
    Structured JSON
           ↓
    Pydantic Validation
           ↓
    Business Rules
           ↓
       PostgreSQL

AI handles the **unstructured → structured** part of the workflow.

The rest remains normal application logic.

## Project Structure

    invoice-automation/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py        # FastAPI endpoints and application logic
    │   ├── database.py    # PostgreSQL connection and sessions
    │   ├── models.py      # SQLAlchemy database models
    │   └── schemas.py     # Pydantic validation schemas
    ├── docker-compose.yml # PostgreSQL container
    ├── requirements.txt
    └── README.md

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Docker
- LLM API

## Getting Started

### Prerequisites

Make sure you have installed:

- Python 3.10+
- Docker Desktop
- Git

### 1. Clone the repository

    git clone <repository-url>
    cd invoice-automation

### 2. Create a virtual environment

#### Windows

    python -m venv venv
    venv\Scripts\activate

#### macOS / Linux

    python3 -m venv venv
    source venv/bin/activate

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Start PostgreSQL

Make sure Docker Desktop is running.

    docker compose up -d

Check that PostgreSQL is running:

    docker ps

### 5. Start the FastAPI application

From the project root:

    uvicorn app.main:app --reload

The API should now be available at:

    http://127.0.0.1:8000

### 6. Open the API documentation

Open the following URL in your browser:

    http://127.0.0.1:8000/docs

FastAPI provides an interactive interface for testing the API.

### 7. Create an invoice

Use `POST /invoices` and provide:

    {
      "supplier": "Microsoft",
      "invoice_number": "INV-1234",
      "invoice_date": "2026-09-01",
      "amount": 1250,
      "currency": "EUR"
    }

Then use `GET /invoices` to verify that the invoice was stored in PostgreSQL.

## Development Plan

- [x] Basic invoice API
- [x] PostgreSQL storage
- [x] Request validation
- [x] Invoice date validation
- [x] Logging
- [x] AI invoice extraction
- [x] AI output validation
- [ ] Human review for uncertain invoices
- [ ] Optional message queue

## Goal

Understand how an LLM can be added to an existing software workflow without replacing the systems that handle **validation, business logic, databases, and APIs**.