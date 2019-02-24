FROM python:3.6-alpine

RUN apk update && apk add build-base libffi-dev
RUN pip install pipenv

ADD . /code
WORKDIR /code

RUN pipenv install --system --deploy

CMD gunicorn --reload --bind 0.0.0.0:8000 knoweak.app:api