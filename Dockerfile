FROM python:3.11-alpine

ARG GIT_COMMIT
ARG GIT_BRANCH=master
ARG GIT_DIRTY=undefined
ARG BUILD_CREATOR
ARG BUILD_NUMBER
ENV flaskenv docker

LABEL branch=$GIT_BRANCH \
    commit=$GIT_COMMIT \
    dirty=$GIT_DIRTY \
    build-creator=$BUILD_CREATOR \
    build-number=$BUILD_NUMBER

WORKDIR /python-docker

RUN apk add build-base

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "/bin/sh", "-c", "./startup.sh", "$ENV" ]