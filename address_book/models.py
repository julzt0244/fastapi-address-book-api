from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from address_book.database import Base


class User(Base):
    __tablename__ = "User"

    id = Column("UserID", Integer, primary_key=True)
    username = Column("Username", String)
    hashed_password = Column("HashedPassword", String)

    address_books = relationship("AddressBook", back_populates="user")


class AddressBook(Base):
    __tablename__ = "AddressBook"

    id = Column("AddressBookID", Integer, primary_key=True)
    name = Column("Name", String)
    user_id = Column("UserID", Integer, ForeignKey("User.UserID"))

    user = relationship("User", back_populates="address_books")
    contacts = relationship("Contact", back_populates="address_book")


class Contact(Base):
    __tablename__ = "Contact"

    id = Column("ContactID", Integer, primary_key=True)
    name = Column("Name", String)
    phone_number = Column("PhoneNumber", String)
    address_book_id = Column(
        "AddressBookID", Integer, ForeignKey("AddressBook.AddressBookID")
    )

    address_book = relationship("AddressBook", back_populates="contacts")
