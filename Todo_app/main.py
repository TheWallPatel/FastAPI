from fastapi import FastAPI, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated
import models
from models import Todos
from database import engine, SessionLocal
from routers import auth, todos , admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


