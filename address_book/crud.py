from typing import Literal, Optional

from sqlalchemy.orm import Session

from address_book import models, schemas
from address_book.auth import get_password_hash

# region User


def get_user(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter_by(username=username).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    new_user = models.User(
        username=user.username.casefold(),
        hashed_password=get_password_hash(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def delete_user(db: Session, username: str):
    db_user = get_user(db, username)
    db.delete(db_user)
    db.commit()


# endregion


# region AddressBook


def get_address_book(
    db: Session, address_book_id: int, user_id: int
) -> Optional[models.AddressBook]:
    # Note this also check if user is the owner, if not, it will return None
    return (
        db.query(models.AddressBook)
        .filter(models.AddressBook.id == address_book_id)
        .filter(models.AddressBook.user_id == user_id)
        .first()
    )


def get_address_book_by_name(
    db: Session, address_book_name: str, user_id: int
) -> Optional[models.AddressBook]:
    return (
        db.query(models.AddressBook)
        .filter(models.AddressBook.name == address_book_name)
        .filter(models.AddressBook.user_id == user_id)
        .first()
    )


def get_address_books(db: Session, user_id: int) -> list[models.AddressBook]:
    return (
        db.query(models.AddressBook).filter(models.AddressBook.user_id == user_id).all()
    )


def create_address_book(
    db: Session, address_book: schemas.AddressBookCreate, user_id: int
) -> models.AddressBook:
    new_address_book = models.AddressBook(
        name=address_book.name,
        user_id=user_id,
    )
    db.add(new_address_book)
    db.commit()
    db.refresh(new_address_book)
    return new_address_book


def update_address_book(
    db: Session, address_book_id: int, user_id: int, new_name: str
) -> Optional[models.AddressBook]:
    db_address_book = get_address_book(db, address_book_id, user_id)

    if db_address_book:
        db_address_book.name = new_name
        db.commit()
        db.refresh(db_address_book)
        return db_address_book
    else:
        return


def delete_address_book(
    db: Session, address_book_id: int, user_id: int
) -> Optional[Literal[True]]:
    db_address_book = get_address_book(db, address_book_id, user_id)

    if db_address_book:
        db.delete(db_address_book)
        db.commit()
        return True
    else:
        return


# endregion


# region Contact


def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


def get_contacts_by_address_book_id(db: Session, address_book_id: int):
    return (
        db.query(models.Contact)
        .filter(models.Contact.address_book_id == address_book_id)
        .all()
    )


def create_contact(db: Session, contact: schemas.ContactCreate):
    new_contact = models.Contact(
        name=contact.name,
        phone_number=contact.phone_number,
        address_book_id=contact.address_book_id,
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    db.delete(db_contact)
    db.commit()


# endregion Contact
