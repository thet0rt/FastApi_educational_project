from typing import Optional
import sys
sys.path.append('..')

from fastapi import HTTPException

from fastapi import Depends, APIRouter
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from routers.auth import get_current_user, get_user_exception


router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Todo(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(min_length=1, max_length=100)
    priority: int = Field(3, gt=0, lt=6, description='The priority must be between 1-5')
    complete: bool = Field(False)


@router.get('/')
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()

@router.get('/todos/user')
async def read_all_by_user(user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    return db.query(models.Todos)\
        .filter(models.Todos.owner_id == user.get('id'))\
        .all()


@router.get('/todo/{todo_id}')
async def read_todo(todo_id: int,
                    user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get('id'))\
        .first()
    if todo_model is not None:
        return todo_model
    raise http_exception()

@router.post('/')
async def create_todo(todo: Todo,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get('id')
    db.add(todo_model)
    db.commit()
    return successful_response(201)

@router.put('/{todo_id}')
async def update_todo(todo_id: int,
                      todo: Todo,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get('id'))\
        .first()
    if todo_model is None:
        raise http_exception()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return successful_response(201)

@router.delete('/{todo_id}')
async def delete_todo(todo_id: int,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get('id'))\
        .first()

    if todo_model is None:
        raise http_exception()
    db.delete(todo_model)
    db.commit()
    return successful_response(200)

def http_exception():
    return HTTPException(status_code=404, detail='Todo not found')

def successful_response(status_code: int):
    return {
        'status_code': status_code,
        'transaction': 'successful'
    }
