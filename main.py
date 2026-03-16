from fastapi import FastAPI
from sqlalchemy.orm import Session
import uuid
import json

from .database import engine, SessionLocal
from .models import Base, Source, ContentChunk, Question, StudentAnswer
from .ingestion import extract_text_from_pdf, chunk_text
from .quiz_generator import generate_quiz_from_chunk
from .adaptive_logic import adjust_difficulty

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Peblo Quiz Engine Running"}


# -----------------------------
# INGEST PDF
# -----------------------------
@app.post("/ingest")
def ingest_pdf(pdf_path: str, subject: str, grade: int):

    db: Session = SessionLocal()

    source_id = str(uuid.uuid4())

    source = Source(id=source_id, subject=subject, grade=grade)

    db.add(source)

    text = extract_text_from_pdf(pdf_path)

    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):

        chunk_id = f"{source_id}_CH_{i}"

        db_chunk = ContentChunk(
            id=chunk_id,
            source_id=source_id,
            topic=subject,
            text=chunk
        )

        db.add(db_chunk)

    db.commit()

    return {"message": "PDF ingested", "chunks_created": len(chunks)}


# -----------------------------
# GENERATE QUIZ
# -----------------------------
@app.post("/generate-quiz")
def generate_quiz():

    db: Session = SessionLocal()

    # limit chunks to avoid too many API calls
    chunks = db.query(ContentChunk).limit(2).all()

    created_questions = 0

    for chunk in chunks:

        questions = generate_quiz_from_chunk(chunk.text)

        for q in questions:

            question = Question(
                chunk_id=chunk.id,
                question=q.get("question"),
                type=q.get("type"),
                options=json.dumps(q.get("options", [])),
                answer=q.get("answer"),
                difficulty=q.get("difficulty", "easy")
            )

            db.add(question)
            created_questions += 1

    db.commit()

    return {"questions_created": created_questions}


# -----------------------------
# GET QUIZ
# -----------------------------
@app.get("/quiz")
def get_quiz(topic: str, difficulty: str):

    db: Session = SessionLocal()

    questions = (
        db.query(Question)
        .join(ContentChunk, Question.chunk_id == ContentChunk.id)
        .filter(ContentChunk.topic == topic)
        .filter(Question.difficulty == difficulty)
        .limit(5)
        .all()
    )

    results = []

    for q in questions:

        results.append({
            "id": q.id,
            "question": q.question,
            "type": q.type,
            "options": json.loads(q.options)
        })

    return results


# -----------------------------
# SUBMIT ANSWER
# -----------------------------
@app.post("/submit-answer")
def submit_answer(student_id: str, question_id: int, selected_answer: str):

    db: Session = SessionLocal()

    question = db.query(Question).filter(Question.id == question_id).first()

    correct = selected_answer == question.answer

    answer = StudentAnswer(
        student_id=student_id,
        question_id=question_id,
        selected_answer=selected_answer,
        correct=str(correct)
    )

    db.add(answer)

    new_difficulty = adjust_difficulty(question.difficulty, correct)

    db.commit()

    return {
        "correct": correct,
        "next_difficulty": new_difficulty
    }


# -----------------------------
# VIEW CHUNKS
# -----------------------------
@app.get("/chunks")
def get_chunks():

    db: Session = SessionLocal()

    chunks = db.query(ContentChunk).all()

    return [
        {
            "chunk_id": c.id,
            "preview": c.text[:200]
        }
        for c in chunks
    ]


# -----------------------------
# VIEW QUESTIONS
# -----------------------------
@app.get("/questions")
def get_questions():

    db: Session = SessionLocal()

    questions = db.query(Question).all()

    return [
        {
            "id": q.id,
            "question": q.question,
            "difficulty": q.difficulty,
            "source_chunk": q.chunk_id
        }
        for q in questions
    ]