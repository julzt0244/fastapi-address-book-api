# A FastAPI project example

A simple Address Book API implemented in FastAPI together with SQLAlchemy, with most relevant tests being done using Pytest.

The API is secured via a reasonably secure JWT implementation using HS256. As such, most endpoints require authentication before use. Each request to an authenticated endpoint requires a "Authorization": "Bearer XXX" where XXX is the access token provided by the "/account/session/" endpoint upon successful login.

API features implemented:
- Each address book holds the name and phone numbers of contacts entries
- Users are able to add new contacts entries to the address book
- Users are able to remove existing contacts entries from the address book
- Users are able to print all contacts in the address book
- Users are able to maintain multiple address books
- Users are able to print out a unique set of all contacts across multiple address books

## API Documentation/Usage
The documentation is located at "/docs". The root path will also redirect to this endpoint. 

An OpenAPI schema is available at "/openapi.json"

Default Login Details:

```
Username: user
Password: password2021
```

## Requirements
- Docker Desktop
- Python 3.9 and above
- "poetry" Python library installed

## Dev Environment - Localhost

- Open a CMD/command line and navigate/cd to the root directory on your dev machine. The below assumes you are running a Windows computer and have the "poetry" library installed:
- Run this command: ```poetry install && poetry run uvicorn address_book.main:app --port 80 --reload```

## Tests

- Open a CMD/command line and navigate/cd to the root directory on your dev machine. The below assumes you are running a Windows computer and have the "poetry" library installed:
- Run this command: ```poetry install && poetry run pytest```

## Deployment - Docker

- Open a CMD/command line and navigate/cd to the root directory,
- Run these commands one by one: 
```
docker build -t addressbook .
docker run -it --name addressbook --rm -p 88:80 addressbook
```
- Open this address in your web browser "localhost:88" or "127.0.0.1:88"
