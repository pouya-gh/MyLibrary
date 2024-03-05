from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import jwt
import bcrypt
import json
from datetime import timedelta, datetime, timezone

from sql import crud, database, models

with open(".env", "r") as env_file:
    file_dict = json.loads(env_file.read())
    SECRET_KEY = file_dict['secret_key']


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def hash_password(password):
    password_as_bytes = bytes(password, "utf-8")
    return bcrypt.hashpw(password_as_bytes, bcrypt.gensalt()).decode("utf-8")

def check_password(password, hashed_password):
    password_as_bytes = bytes(password, 'utf-8')
    hashed_password_as_bytes = bytes(hashed_password, 'utf-8')
    return bcrypt.checkpw(password_as_bytes, 
                          hashed_password_as_bytes)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)], 
        db: Annotated[Session, Depends(get_db)]):
    credintials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credintials_exception
    except jwt.exceptions.InvalidTokenError:
        raise credintials_exception
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise credintials_exception
    return user

def get_current_active_user(
        current_user: Annotated[models.User, Depends(get_current_user)]
        ):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
