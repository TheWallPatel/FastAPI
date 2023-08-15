from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status


app = FastAPI()
class Book:
    id: int
    title: str
    author: str
    description:str
    rating: str
    published_year : int

    def __init__(self, id, title,author,description,rating, published_year) :
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year

class BookRequest(BaseModel):
    id : Optional[int] = Field(title="id is not need")
    title : str = Field(min_length=3, max_length=30)
    author : str = Field(min_length=3, max_length=30)
    description: str = Field(min_length=3, max_length=30)
    rating : int = Field(gt = 0, lt=6)
    published_year : int = Field(gt= 2000, lt= 2099)

    class Config:
        schema_extra = {
            'example' : {
                'title' : 'A new book',
                'author' : 'author name',
                'description' : 'describe your book',
                'rating' : 'rating between 0 to 5',
                'published_year' : 'Year of book published'
            }

        }


BOOKS = [

    Book(1, "Computer Science Pro 1", 'SHQ', "A very nice book", 5, 2010),
    Book(2, "Computer Science Pro 2", 'SHQ', "A very nice book", 5, 2011),
    Book(3, "Computer Science Pro 3", 'SHQ', "A very nice book", 5, 2012),
    Book(4, "Computer Science Pro 4", 'SHQ', "A very nice book", 5, 2013)
]

@app.get('/books', status_code= status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def read_book_by_id(book_id : int = Path(gt= 0)): # book_id of type of integer, Path is validator
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item is not Available")
 

@app.get('/books/published/{published_year}')
async def read_book_by_published_year(published_year : int = Path(gt= 2000, lt= 2099)):  # published_year of type interger
    books_to_return = []
    for book in BOOKS:
        if book.published_year == published_year:
            books_to_return.append(book)

    return books_to_return

@app.get('/books/rating/{book_rating}')
async def read_book_by_rating(book_rating: int = Path(gt=0,lt=6)):  # book_rating of type integer
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return


@app.post('/create-book', status_code=status.HTTP_201_CREATED)
# pydantic validation using class BookRequest
async def create_book(book_request: BookRequest): # book_request is of type BookRequest
    # print(type(book_request))
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id +1
    return book

@app.put('/books/update_book', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book : BookRequest): # book of type BookRequest
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
        
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt = 0)):  # book_id is of type integer
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")


# data validation