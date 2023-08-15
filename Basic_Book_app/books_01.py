# this is Project 1
from fastapi import FastAPI, Body

app = FastAPI()

Books = [
    {'title' : "Title One", 'author' : 'author One'},
    {'title' : "Title Two", 'author' : 'author Two'},
    {'title' : "Title Three", 'author' : 'author Three'},
]

@app.get('/api-endpoint')
async def first_api():
    return {"message" : "Hello Dhawal", "data" : Books}
    # return Books

@app.get('/books')
async def read_all_books():
    return Books

@app.get('/books/firstbook')
async def read_all_books():
    # print(dynamic_data)
    return Books[0]

@app.get('/books/{dynamic_data}')
async def read_all_books(dynamic_data):
    print(dynamic_data)
    for book in Books:
        if book["title"].casefold() == dynamic_data:
            return book
        
    return None

#query parameter
# http://127.0.0.1:8000/books/?authorname=author%20one
@app.get('/books/')
async def read_author(author: str):
    print(author)
    for book in Books:
        if book['author'].casefold() == author.casefold():
            return book
        
    return None


##### for Post request methods
@app.post('/books/create_book')
async def post_book(new_book = Body()):
    Books.append(new_book)


# for PUT Request
@app.put('/books/updatebook')
async def update_book(book_to_update = Body()):
    # find the dict where title matches then replace the dict to new dict
    for i in range(len(Books)):
        if Books[i]['title'].casefold() == str(book_to_update.get('title')).casefold():
            Books[i] = book_to_update
            return Books[i]
    return None

# for Delete Request
@app.delete('/books/delete/{book_title}')
async def delete_book(book_title : str):
    for i in range(len(Books)):
        if Books[i].get('title').casefold() == book_title.casefold():
           Books.pop(i)
           return "delete successfully"

    return None 

"""
assignment 1 
1. Create a new API Endpoint that can fetch all books from
 a specific author using either Path Parameters or Query Parameters.

"""

@app.post('/createbooks/')
async def create_author_books(book_author : str , category : str):
    print(book_author, category)
    return "success"

