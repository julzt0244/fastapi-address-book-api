from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from address_book import crud, database, models, schemas
from address_book.database import SessionLocal
from address_book.routers import account, address_books, contacts

description = """
Please click the above link to download the OpenAPI schema.

Data is persisted using SQLite via SQLAlchemy and is stored in the root folder as AddressBookDB.db. (Or TestDB.db when running tests)

Authentication is done via JWT Tokens and the private key for it is stored as a SECRET_KEY.txt file in the root folder (or generated if absent).

Default Login Details:

```
Username: user
Password: password2021
```

"""

app = FastAPI(
    title="Address Book API",
    version="1.0",
    description=description,
    contact={
        "name": "Julian Tan",
        "email": "julian.tanz@yahoo.com",
    },
)
app.include_router(account.router)
app.include_router(address_books.router)
app.include_router(contacts.router)


@app.on_event("startup")
def start_db():
    models.Base.metadata.create_all(bind=database.engine)
    create_default_user_if_none_exists()


def create_default_user_if_none_exists():
    # Just so we can start with a default user instead of having to register
    default_username = "user"
    default_password = "password2021"

    db = SessionLocal()
    result = crud.get_user(db, default_username)
    if result is None:
        crud.create_user(db, schemas.UserCreate(username=default_username, password=default_password))


@app.get("/", tags=["Other"])
def root():
    """
    Redirect users to the API documentation page.
    """
    return RedirectResponse(url="/docs")
