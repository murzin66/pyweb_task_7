from fastapi import FastAPI, Query, HTTPException, Depends
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Инициализация SQLAlchemy
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Модель терминов
class TermInDB(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, index=True)
    definition = Column(String)
    priority = Column(Integer)
    relation = Column(Integer, nullable=True)


# Создание таблиц
Base.metadata.create_all(bind=engine)

# Создание экземпляра FastAPI
app = FastAPI()


# Pydantic модель для запросов
class Term(BaseModel):
    term: str
    definition: str
    priority: int
    relation: Optional[int] = None

    class Config:
        orm_mode = True


# Получение базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Получение всех терминов
@app.get("/terms", response_model=List[Term])
async def get_all_terms(db: Session = Depends(get_db)):
    terms = db.query(TermInDB).all()
    return terms


# Добавление нового термина
@app.post("/add/", response_model=Term)
async def create_term(term: Term, db: Session = Depends(get_db)):
    db_term = TermInDB(term=term.term, definition=term.definition, priority=term.priority, relation=term.relation)
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return db_term


# Модификация существующего термина
@app.put("/modify/{term_id}", response_model=Term)
async def modify_term(term_id: int, changed_term: Term, db: Session = Depends(get_db)):
    db_term = db.query(TermInDB).filter(TermInDB.id == term_id).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Term not found")

    db_term.term = changed_term.term or db_term.term
    db_term.definition = changed_term.definition or db_term.definition
    db_term.priority = changed_term.priority or db_term.priority
    db_term.relation = changed_term.relation or db_term.relation

    db.commit()
    db.refresh(db_term)
    return db_term


# Получение термина по ID
@app.get("/term/{term_id}", response_model=Term)
async def get_term(term_id: int, db: Session = Depends(get_db)):
    db_term = db.query(TermInDB).filter(TermInDB.id == term_id).first()
    if db_term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    return db_term


# Удаление термина
@app.delete("/delete/{term_id}")
async def delete_term(term_id: int, db: Session = Depends(get_db)):
    db_term = db.query(TermInDB).filter(TermInDB.id == term_id).first()
    if db_term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    db.delete(db_term)
    db.commit()
    return {"message": f"Term {term_id} deleted successfully"}


# Стартовая страница
@app.get('/about')
async def about():
    return {"about": "DictionaryApp"}


# Информация об авторе
@app.get('/author')
async def author():
    return {"author": "Murzin Michael"}


# Инициализация базы данных начальными терминами
@app.on_event("startup")
async def startup():
    db = SessionLocal()
    try:
        # Начальные термины
        initial_terms = [
            {"term": "Система управления обучением (LMS)", "definition": "Платформа или программное обеспечение для интеграции инструментов обучения", "priority": 1},
            {"term": "Граф знаний", "definition": "Коллекция взаимосвязанных сущностей и их описаний", "priority": 2},
            {"term": "Онтология", "definition": "Семантическая модель данных, описывающая сущности реального мира", "priority": 3},
            {"term": "Стемминг", "definition": "Поиск формы слова, учитывающий морфологию исходного слова", "priority": 4},
            {"term": "Индуктивные методы заполнения графа знаний", "definition": "Методы предсказания отсутствующих триплетов между новыми сущностями", "priority":5},
            {"term": "Дедуктивные методы заполнения графа знаний", "definition": "Методы, основанные на сопоставлении сущностей и отношений между ними с помощью формальных правил", "priority":6},
            {"term": "Гетерогенный граф", "definition": "Граф с различными типами узлов и рёбер", "priority": 7},
            {"term": "Граф свойств", "definition": "Тип графовой модели, в которой отношения имеют имя и свойства", "priority": 8},
            {"term": "Семантическая схема", "definition": "Схема, определяющая значение высокоуровневых терминов и иерархию классов", "priority": 9},
            {"term": "Валидирующая схема", "definition": "Схема, описывающая минимальный набор данных для обеспечения полноты графа знаний", "priority": 10},
            {"term": "Эмерджентная схема", "definition": "Схема, описывающая скрытые структуры графа знаний", "priority": 11},
            {"term": "Ризонинг", "definition": "Технология выявления новых связей между сущностями в графе знаний", "priority": 12},
            {"term": "Эмбеддинг", "definition": "Векторное представление сущностей графа знаний и отношений между ними", "priority": 13},
            {"term": "GraphQL", "definition": "Язык запросов к API и среда выполнения для выполнения этих запросов", "priority": 14},
            {"term": "REST", "definition": "Архитектурный стиль для разработки веб-сервисов и систем", "priority": 15},
            {"term": "DBpedia", "definition": "Проект по извлечению структурированного контента из Википедии", "priority": 16},

        ]

        for term_data in initial_terms:
            term = db.query(TermInDB).filter(TermInDB.term == term_data["term"]).first()
            if not term:
                db.add(TermInDB(**term_data))
        db.commit()
    finally:
        db.close()
