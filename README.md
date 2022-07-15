# A FastAPI project example

A simple Address Book API implemented in FastAPI. Most endpoints require authentication before use. Each request to an authenticated endpoint requires a "Authorization": "Bearer XXX" where XXX is the access token provided by the "/account/session/" endpoint upon successful login.

Default Login Details:

```
Username: user
Password: password2021
```

## Usage 
The documentation is located at "/docs". The root path will also redirect to this endpoint. 

An OpenAPI schema is available at "/openapi.json"

## Deployment - Docker

- Open a CMD/command line and navigate/cd to the root directory,
- Run this command: ```docker build -t addressbook .```
- Run this command: ```docker run -p 80:80 addressbook```
- Open this address in your web browser "localhost" or "127.0.0.1"

## Dev Environment - Localhost

- Open a CMD/command line and navigate/cd to the root directory on your dev machine. The below assumes you are running a Windows computer and have the "poetry" library installed:
- Run this command: ```poetry install && poetry run uvicorn address_book.main:app --port 80 --reload```

## Tests

- Open a CMD/command line and navigate/cd to the root directory on your dev machine. The below assumes you are running a Windows computer and have the "poetry" library installed:
- Run this command: ```poetry install && poetry run pytest```
