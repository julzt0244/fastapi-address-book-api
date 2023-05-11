from typing import Any, List, Optional

from pydantic import BaseModel, Field

from address_book.utils import to_camel_case

# region Token


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# endregion


# region User


class UserBase(BaseModel):
    username: str = Field(..., example="newuser")

    class Config:
        orm_mode = True
        alias_generator = to_camel_case
        allow_population_by_field_name = True


class UserCreate(UserBase):
    password: str = Field(..., example="newpassword", min_length=8, max_length=100)


class User(UserBase):
    id: int = Field(..., ge=1)
    address_books: List[Any]


# endregion


# region AddressBook


class AddressBookBase(BaseModel):
    name: str = Field(..., example="Default Profile")

    class Config:
        orm_mode = True
        alias_generator = to_camel_case
        allow_population_by_field_name = True


class AddressBookCreate(AddressBookBase):
    pass


class AddressBookUpdate(AddressBookBase):
    pass


class AddressBookDelete(AddressBookBase):
    pass


class AddressBook(AddressBookBase):
    id: int = Field(..., ge=1)
    contacts: List[Any]


# endregion


# region Contact


class ContactBase(BaseModel):
    name: str
    phone_number: str

    class Config:
        orm_mode = True
        alias_generator = to_camel_case
        allow_population_by_field_name = True


class ContactCreate(ContactBase):
    address_book_id: int


class Contact(ContactBase):
    id: int = Field(..., ge=1)
    address_book_id: int


# endregion
