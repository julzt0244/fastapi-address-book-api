from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from address_book import auth, database, models

GetDb = Annotated[Session, Depends(database.get_db)]
GetUser = Annotated[models.User, Depends(auth.get_current_user)]