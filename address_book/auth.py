from base64 import b64encode
from datetime import datetime, timedelta
from secrets import token_bytes
from typing import Any, Dict, Optional, cast

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from address_book import crud, database, models, schemas

# Simple storage of secret key in a txt file, make sure this file is always in .gitignore
try:
    with open("SECRET_KEY.txt") as file:
        SECRET_KEY = file.read()
except Exception:
    print("""No SECRET_KEY.txt file found. Generating a new one in the root directory""")
    with open("SECRET_KEY.txt", "w") as file:
        SECRET_KEY = b64encode(token_bytes(32)).decode()  # type: ignore
        file.write(SECRET_KEY)


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 90


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="account/session/")


def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user(db, username)
    if not user:
        return False
    if not verify_password(password, cast(str, user.hashed_password)):
        return False
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return cast(bool, pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    return cast(str, pwd_context.hash(password))


def create_access_token(data: Dict[Any, Any], expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
