from sqlalchemy import Column, Integer, String, Text, ForeignKey
from .database import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(String, primary_key=True)
    subject = Column(String)
    grade = Column(Integer)


class ContentChunk(Base):
    __tablename__ = "content_chunks"

    id = Column(String, primary_key=True)
    source_id = Column(String, ForeignKey("sources.id"))
    topic = Column(String)
    text = Column(Text)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chunk_id = Column(String)
    question = Column(Text)
    type = Column(String)
    options = Column(Text)
    answer = Column(String)
    difficulty = Column(String)


class StudentAnswer(Base):
    __tablename__ = "student_answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String)
    question_id = Column(Integer)
    selected_answer = Column(String)
    correct = Column(String)