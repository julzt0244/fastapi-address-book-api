from typing import List, cast

from fastapi import APIRouter, HTTPException, status

from address_book import crud, schemas
from address_book.routers.shared_dependencies import GetDb, GetUser

router = APIRouter(
    prefix="/address-books",
    tags=["AddressBooks"],
)


@router.post("/", response_model=schemas.AddressBook)
def create_address_book(
    address_book: schemas.AddressBookCreate, db: GetDb, current_user: GetUser
):
    current_user_id = cast(int, current_user.id)

    db_address_book = crud.get_address_book_by_name(
        db, address_book.name, current_user_id
    )
    if db_address_book:
        raise HTTPException(
            status_code=409, detail="An AddressBook with that name already exists"
        )
    return crud.create_address_book(db, address_book, current_user_id)


@router.get("/", response_model=List[schemas.AddressBook])
def read_address_books(db: GetDb, current_user: GetUser):
    current_user_id = cast(int, current_user.id)
    return crud.get_address_books(db, current_user_id)


@router.get("/{address_book_id}", response_model=schemas.AddressBook)
def read_address_book(address_book_id: int, db: GetDb, current_user: GetUser):
    current_user_id = cast(int, current_user.id)
    address_book = crud.get_address_book(db, address_book_id, current_user_id)
    if address_book is None:
        raise HTTPException(status_code=404, detail="AddressBook not found")
    return address_book


@router.put("/{address_book_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_address_book(
    address_book_id: int,
    address_book: schemas.AddressBookUpdate,
    db: GetDb,
    current_user: GetUser,
):
    current_user_id = cast(int, current_user.id)
    db_address_book = crud.update_address_book(
        db, address_book_id, current_user_id, address_book.name
    )
    if db_address_book is None:
        raise HTTPException(status_code=404, detail="AddressBook not found")
    return


@router.delete("/{address_book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address_book(address_book_id: int, db: GetDb, current_user: GetUser):
    current_user_id = cast(int, current_user.id)
    address_book = crud.delete_address_book(db, address_book_id, current_user_id)
    if address_book:
        return
    else:
        raise HTTPException(status_code=404, detail="AddressBook not found")
