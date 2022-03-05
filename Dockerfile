FROM python:3.7.12-buster

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY ./api/ /code/

RUN apt update && apt install -y locales
RUN sed -i -e 's/# es_MX.UTF-8 UTF-8/es_MX.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LC_ALL es_MX.UTF-8 
ENV LANG es_MX.UTF-8  
ENV LANGUAGE es_MX:es

RUN pip install pipenv && python -m pip install --upgrade pip && pipenv install --system

EXPOSE 8000

