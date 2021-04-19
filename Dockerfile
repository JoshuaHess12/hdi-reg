FROM python:3.7

RUN pip install pathlib numpy

COPY . /app/
