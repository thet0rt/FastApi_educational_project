from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title='Description of the book',
                             min_length=1,
                             max_length=100)
    rating: int = Field(gt=-1, lt=101)



BOOKS =[]

@app.get('/')
async def read_all_books():
    if len(BOOKS) < 1:
        create_book_no_api()
    return BOOKS

@app.post('/')
async def create_book(book: Book):
    BOOKS.append(book)
    return book

def create_book_no_api():
    book_1 = Book(id='82c19c62-ce42-4b88-8dd9-8b5e408c2ba6',
                  title='Title 1',
                  author='Author 1',
                  description='Description 1',
                  rating=60)
    book_2 = Book(id='ef90757d-9a0e-40ca-8d16-bc2c398f96fe',
                  title='Title 2',
                  author='Author 2',
                  description='Description 2',
                  rating=70)
    book_3 = Book(id='941fe7e9-b013-4c0a-82e0-d3d8f8e5d8a3',
                  title='Title 3',
                  author='Author 3',
                  description='Description 3',
                  rating=80)
    book_4 = Book(id='3c43f07f-5ceb-47c7-bc6a-3401b8850d92',
                  title='Title 4',
                  author='Author 4',
                  description='Description 4',
                  rating=90)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)











