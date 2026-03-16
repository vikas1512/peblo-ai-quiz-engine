# Peblo AI Backend Engineer Challenge

This project implements a prototype backend system that ingests educational PDF content and converts it into quiz questions using an LLM.

The system demonstrates how educational material can be transformed into adaptive quizzes through AI-powered content processing.

---

# Architecture Overview

PDF → Text Extraction → Chunking → LLM Quiz Generation → Database Storage → API Retrieval → Adaptive Difficulty

---

# Tech Stack

Backend Framework  
FastAPI

Database  
SQLite

LLM Provider  
Groq API (LLaMA 3.1)

Libraries
- pdfplumber
- SQLAlchemy
- python-dotenv
- groq

---

# System Components

## 1. Content Ingestion

The system ingests educational PDF files and extracts raw text.

Steps:
1. Read PDF using pdfplumber
2. Clean extracted text
3. Split content into chunks
4. Store chunks in database

Example chunk format:


{
"source_id": "SRC_001",
"chunk_id": "SRC_001_CH_01",
"subject": "Science",
"text": "Plants need sunlight, water and air..."
}


---

## 2. Quiz Generation

Chunks are sent to an LLM which generates quiz questions.

Question types supported:
- Multiple Choice Questions (MCQ)
- True/False
- Fill in the Blank

Example generated question:


{
"question": "What do plants need to survive?",
"type": "MCQ",
"options": ["Sunlight", "Metal", "Plastic", "Sand"],
"answer": "Sunlight",
"difficulty": "easy"
}


Each question stores the `source_chunk_id` for traceability.

---

## 3. Quiz Retrieval API

Users can request quizzes based on topic and difficulty.

Example endpoint:


GET /quiz?topic=Science&difficulty=easy


---

## 4. Student Answer Submission

Students submit answers through the API.

Example request:


POST /submit-answer
{
"student_id": "S001",
"question_id": 1,
"selected_answer": "Sunlight"
}


---

## 5. Adaptive Difficulty

Difficulty adjusts dynamically:

Correct answer → increase difficulty  
Incorrect answer → decrease difficulty

This simulates adaptive learning behaviour.

---

# API Endpoints

| Endpoint | Method | Description |
|--------|--------|-------------|
| / | GET | Health check |
| /ingest | POST | Upload and process PDF |
| /generate-quiz | POST | Generate questions using LLM |
| /quiz | GET | Retrieve quiz questions |
| /submit-answer | POST | Submit student answers |
| /chunks | GET | View extracted chunks |
| /questions | GET | View generated questions |

---

# Installation

Clone repository:


git clone https://github.com/YOURNAME/peblo-ai-quiz-engine.git

cd peblo-ai-quiz-engine


Create virtual environment:


python -m venv venv
source venv/bin/activate


Install dependencies:


pip install -r requirements.txt


---

# Environment Variables

Create a `.env` file:


GROQ_API_KEY=your_api_key
DATABASE_URL=sqlite:///quiz.db


---

# Running the Backend

Start the FastAPI server:


uvicorn app.main:app --reload


Open API documentation:


http://127.0.0.1:8000/docs


---

# Example Workflow

1. Upload PDF using `/ingest`
2. Generate quiz questions using `/generate-quiz`
3. Retrieve questions using `/quiz`
4. Submit answers using `/submit-answer`
5. Difficulty adjusts based on performance

---

# Demo

The demo video demonstrates:

- PDF ingestion
- Chunk extraction
- Quiz generation using LLM
- Quiz retrieval
- Adaptive difficulty behaviour

---
