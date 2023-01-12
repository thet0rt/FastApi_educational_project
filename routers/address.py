import sys
sys.path.append('..')

from typing import Optional
from fastapi import Depends, APIRouter, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user, get_user_exception

router = APIRouter(
    prefix = '/address',
    tags = ['address'],
    responses = {404: {'description': 'Not found'}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Address(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    country: str
    postalcode: str

@router.post('/')
async def add_address(
        address: Address,
        user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    if address is None:
        raise HTTPException(404, 'Wrong data')
    new_address = models.Address()
    new_address.address1 = address.address1
    new_address.address2 = address.address2
    new_address.state = address.state
    new_address.city = address.city
    new_address.country = address.country
    new_address.postalcode = address.postalcode

    db.add(new_address)
    db.flush()

    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()

    user_model.address_id = new_address.id
    db.add(user_model)
    db.commit()

    return 200


