from typing import List, Set, Tuple, cast

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from address_book import auth, crud, database, models, schemas

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"],
)


@router.post("/", response_model=schemas.Contact)
def create_contact(user: schemas.ContactCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    output = crud.create_contact(db, user)
    return output


@router.get("/", response_model=List[schemas.ContactBase])
def read_contacts(unique: bool = False, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_address_books = crud.get_address_books(db, cast(int, current_user.id))

    output: List[schemas.ContactBase] = []

    if unique:
        unique_data_set: Set[Tuple[str, str]] = set()
        for address_book in db_address_books:
            db_contacts = crud.get_contacts_by_address_book_id(db, cast(int, address_book.id))
            name_and_phone_numbers_only = [(i.name, i.phone_number) for i in db_contacts]

            for val in name_and_phone_numbers_only:
                unique_data_set.add(val)

        for data in unique_data_set:
            output.append(schemas.ContactBase(name=data[0], phone_number=data[1]))

    else:
        for address_book in db_address_books:
            db_contacts = crud.get_contacts_by_address_book_id(db, cast(int, address_book.id))
            output.extend(db_contacts)

    return output


@router.get("/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_contact = crud.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    if current_user != db_contact.address_book.user:
        raise HTTPException(status_code=403, detail="You do not have access to that Contact")
    return db_contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_contact = crud.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    if current_user != db_contact.address_book.user:
        raise HTTPException(status_code=403, detail="You do not have access to that Contact")
    crud.delete_contact(db, contact_id)
    return
