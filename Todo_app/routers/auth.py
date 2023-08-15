from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from models import Users
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "8bffd6ffbb926ea5a1b665de543db92bbf925364f8be0c181ba63a992047532d"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username ).first()
    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    else:
        return user
        
def create_access_token(username:str, user_id : int, role:str ,expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expire = datetime.utcnow() + expires_delta
    encode.update({'exp' : expire})

    return jwt.encode(encode, SECRET_KEY, algorithm= ALGORITHM )

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id : int = payload.get('id')
        user_role :str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details= 'Could not validate user')
        
        return {"username": username, 'id' : user_id, 'role' : user_role}
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details= 'Could not validate user')
        




class CreateUserRequest(BaseModel):
    username : str
    email : str
    firstname : str
    lastname : str
    password : str
    role : str    

class Token(BaseModel):
    access_token : str
    token_type : str


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency):
    return db.query(Users).all()    

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        
        email = create_user_request.email,
        username = create_user_request.username,
        firstname = create_user_request.firstname,
        lastname = create_user_request.lastname,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True
    )
    
    db.add(create_user_model)
    db.commit()

    return create_user_model

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                  db:db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= 'Could not validate user')

    token = create_access_token( user.username, user.id, user.role, timedelta(minutes=20) )
    return {'access_token' : token, 'token_type' : "bearer"}
