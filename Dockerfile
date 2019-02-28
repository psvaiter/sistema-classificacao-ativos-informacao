FROM python:3.6-alpine

RUN apk update && apk add build-base libffi-dev
RUN pip install pipenv

COPY . /code

WORKDIR /code
RUN pipenv install --system --deploy

CMD gunicorn knoweak.app:api