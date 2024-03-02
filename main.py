from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from sql import crud, models, schemas
from sql.database import SessionLocal, engine
from dependencies import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
async def index():
    return {"msg": "Welcome!"}

@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User email/username already exists")

@app.get("/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_user

@app.post("/users/{user_id}", response_model=schemas.User)
def update_user(data: schemas.UserUpdate, user_id: int, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_user

@app.post("/users/{user_id}/delete", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_user