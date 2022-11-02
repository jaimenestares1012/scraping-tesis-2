FROM python:3.6-slim

WORKDIR /code

COPY ./requeriment.txt /code

RUN pip install -r requeriment.txt

COPY . /code

EXPOSE  5000
