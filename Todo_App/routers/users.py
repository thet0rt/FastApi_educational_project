from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from routers.todos import get_db, successful_response
import models
from routers.auth import get_current_user, get_user_exception, verify_password, get_password_hash

router = APIRouter(
    prefix='/users',
    tags=['/users'],
    responses={418: {'description': 'Method is not allowed'}}
)


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


@router.get('/')
async def get_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

@router.get('/{username}')
async def get_user(username: str = None,
                   db: Session = Depends(get_db)):
    if username is None:
        raise HTTPException(status_code=404, detail='User not found')
    result = db.query(models.Users).filter(models.Users.username == username).first()
    if result is None:
        raise HTTPException(status_code=404, detail='User not found')
    return result

@router.get('/get_certain_user/')
async def get_certain_user(username: str,
                           db: Session = Depends(get_db)):
    if username is None:
        raise HTTPException(status_code=404, detail='User not found')
    result = db.query(models.Users).filter(models.Users.username == username).first()
    if result is None:
        raise HTTPException(status_code=403, detail='User not found')
    return result

@router.patch('/change_password/')
async def change_password(user_verification: UserVerification,
                          user: dict = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    result = db.query(models.Users).filter(models.Users.username == user.get('username')).first()
    if result is None:
        raise HTTPException(404, detail='User not found')
    if not (verify_password(user_verification.password, result.hashed_password)):
        raise HTTPException(404, detail='Old password doesnt match')
    new_password_hashed = get_password_hash(user_verification.new_password)
    db.query(models.Users)\
        .filter(models.Users.username == user.get('username'))\
        .update({models.Users.hashed_password: new_password_hashed})
    db.commit()
    return successful_response(200)

@router.delete('/')
async def delete_user(
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)):
    if user is None:
        raise get_user_exception()
    result = db.query(models.Users).filter(models.Users.username == user.get('username')).first()
    fkey = result.id
    db.query(models.Todos).filter(models.Todos.owner_id == fkey).delete()
    db.query(models.Users).filter(models.Users.username == user.get('username')).delete()
    db.commit()

