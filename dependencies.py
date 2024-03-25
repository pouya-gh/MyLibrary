from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi import Depends, HTTPException, Security, status
from sqlalchemy.orm import Session
from pydantic import ValidationError, BaseModel

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

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='token',
    scopes={"super": "permission to perform administrator action"},)

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
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(oauth2_scheme)], 
        db: Annotated[Session, Depends(get_db)]):
    
    if security_scopes.scopes:
        authenticate_value = f"Bearer scopes=\"{security_scopes.scope_str}\""
    else:
        authenticate_value = "Bearer"
    credintials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credintials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
    except (jwt.exceptions.InvalidTokenError, ValidationError):
        raise credintials_exception
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise credintials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
                        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user

def get_current_active_user(
        current_user: Annotated[models.User, Depends(get_current_user)]
        ):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
