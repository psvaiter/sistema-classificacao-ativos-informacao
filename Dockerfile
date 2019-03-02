FROM python:3.6-alpine

RUN apk update && apk add build-base libffi-dev
RUN pip install pipenv

COPY Pipfile Pipfile.lock /
RUN pipenv install --system --deploy

COPY ./knoweak /knoweak

CMD gunicorn knoweak.app:api