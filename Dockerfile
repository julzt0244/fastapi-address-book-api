FROM python:3.9-slim

RUN apt-get update && apt-get upgrade -y

# Install python and libs
RUN apt-get install -y -q git
RUN pip install gunicorn uvloop httptools

# Install Poetry
RUN pip install poetry==1.4.2
RUN export PATH="$HOME/.local/bin:$PATH"

# Copy across project code and install to system Python
RUN mkdir /app
COPY ./pyproject.toml ./poetry.lock ./poetry.toml /app
RUN mkdir /app/address_book
COPY ./address_book /app/address_book

WORKDIR /app
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-dev

# Run server
ENTRYPOINT /usr/local/bin/gunicorn \
    address_book.main:app \
    -b 0.0.0.0:80 \
    --chdir /app/ \ 
    -w 4 -k uvicorn.workers.UvicornWorker