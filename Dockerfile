# Pull base image
FROM python:3.8.0

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
WORKDIR /code/

COPY . /code/
EXPOSE 8080
