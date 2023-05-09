FROM python:3.9-slim

RUN apt-get update && apt-get upgrade -y

# Install python and libs
RUN apt-get install -y -q git
RUN pip install gunicorn uvloop httptools

# Install Poetry
RUN pip install poetry==1.4.2
RUN export PATH="$HOME/.local/bin:$PATH"

# Pull from git and install reqs
RUN git clone https://github.com/julzt0244/fastapi-address-book-api.git /app
WORKDIR /app
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-dev

# Run server
ENTRYPOINT /usr/local/bin/gunicorn \
    address_book.main:app \
    -b 0.0.0.0:80 \
    --chdir /app/ \ 
    -w 4 -k uvicorn.workers.UvicornWorker \