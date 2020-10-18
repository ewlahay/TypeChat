FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN mkdir /app/data
COPY ./app/dist /app/app/dist
COPY *.py /app/
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt