FROM python:3.9-slim

RUN apt update && apt upgrade -y

# Install python and libs
RUN apt install -y -q git
RUN pip3 install gunicorn uvloop httptools

# Pull from git and install reqs
RUN git clone https://github.com/julzt0244/fastapi-address-book-api.git /app
RUN pip3 install -r /app/requirements.txt

# Run server
ENTRYPOINT /usr/local/bin/gunicorn \
    address_book.main:app \
    -b 0.0.0.0:80 \
    --chdir /app/ \ 
    -w 4 -k uvicorn.workers.UvicornWorker \