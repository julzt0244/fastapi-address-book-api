from datetime import timedelta
from typing import cast
import random

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from address_book import auth, crud, database, models, schemas
from address_book.exception_handler import RouteErrorHandler
from address_book.exceptions import MyCustomException

router = APIRouter(
    prefix="/account",
    tags=["Account Operations"],
    route_class=RouteErrorHandler
)


@router.get("/", response_model=schemas.User)
def get_user_account_info(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


@router.post("/", response_model=schemas.User)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, new_user.username.casefold())
    # Demonstrating a randomly raised custom exception that is handled by the exception_handler.py
    if random.randint(1, 3) == 1:
        raise MyCustomException("MEOW")
    if db_user:
        raise HTTPException(status_code=409, detail="That username is already taken")
    return crud.create_user(db, new_user)


@router.post("/session/", response_model=schemas.Token)
def login_user(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username.casefold(), form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=auth.ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    crud.delete_user(db, cast(str, current_user.username))
    return
