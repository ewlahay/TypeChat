FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY ./app/dist /app/app/dist
COPY *.py /app/
COPY requirements.txt /app/requirements.txt
RUN mkdir /app/data && pip install -r /app/requirements.txt