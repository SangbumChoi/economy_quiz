from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db, Quiz, create_tables
from pydantic import BaseModel
from typing import List, Optional
import random
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="경제 퀴즈 API", version="1.0.0")

# Create tables on startup with retry logic
@app.on_event("startup")
def startup_event():
    max_retries = 30
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            logger.info(f"데이터베이스 연결 시도 {attempt + 1}/{max_retries}")
            create_tables()
            logger.info("데이터베이스 테이블 생성 완료")
            break
        except Exception as e:
            logger.warning(f"데이터베이스 연결 실패 (시도 {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logger.error("데이터베이스 연결에 실패했습니다. 서버를 계속 실행합니다.")
                # Don't fail the startup, let the app run and handle DB errors gracefully

# Pydantic models
class QuizResponse(BaseModel):
    id: int
    question: str
    answer: bool
    explanation: Optional[str] = None
    category: Optional[str] = None
    difficulty: str

class QuizCreate(BaseModel):
    question: str
    answer: bool
    explanation: Optional[str] = None
    category: Optional[str] = None
    difficulty: str = "medium"

class QuizUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[bool] = None
    explanation: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None

# API Routes
@app.get("/")
async def read_root():
    return HTMLResponse(open("templates/index.html", "r", encoding="utf-8").read())

@app.get("/api/quizzes", response_model=List[QuizResponse])
async def get_quizzes(
    skip: int = 0, 
    limit: int = 10, 
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Quiz)
    
    if category:
        query = query.filter(Quiz.category == category)
    if difficulty:
        query = query.filter(Quiz.difficulty == difficulty)
    
    quizzes = query.offset(skip).limit(limit).all()
    return quizzes

@app.get("/api/quizzes/random", response_model=QuizResponse)
async def get_random_quiz(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Quiz)
    
    if category:
        query = query.filter(Quiz.category == category)
    if difficulty:
        query = query.filter(Quiz.difficulty == difficulty)
    
    quizzes = query.all()
    if not quizzes:
        raise HTTPException(status_code=404, detail="퀴즈를 찾을 수 없습니다.")
    
    return random.choice(quizzes)

@app.get("/api/quizzes/{quiz_id}", response_model=QuizResponse)
async def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="퀴즈를 찾을 수 없습니다.")
    return quiz

@app.post("/api/quizzes", response_model=QuizResponse)
async def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
    db_quiz = Quiz(**quiz.dict())
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

@app.put("/api/quizzes/{quiz_id}", response_model=QuizResponse)
async def update_quiz(quiz_id: int, quiz: QuizUpdate, db: Session = Depends(get_db)):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="퀴즈를 찾을 수 없습니다.")
    
    update_data = quiz.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_quiz, field, value)
    
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

@app.delete("/api/quizzes/{quiz_id}")
async def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="퀴즈를 찾을 수 없습니다.")
    
    db.delete(db_quiz)
    db.commit()
    return {"message": "퀴즈가 삭제되었습니다."}

@app.get("/api/categories")
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Quiz.category).filter(Quiz.category.isnot(None)).distinct().all()
    return [cat[0] for cat in categories]

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT
    uvicorn.run(app, host=API_HOST, port=API_PORT)
