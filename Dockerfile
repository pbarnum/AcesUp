# Project: AcesUp
# Author: Patrick Barnum <patrickdbarnum@gmail.com>
# Created: 2017-10-14

FROM python:jessie

LABEL maintainer='patrickdbarnum@gmail.com'

COPY . /acesup

WORKDIR /acesup

RUN pip install --no-cache-dir -r requirements.txt
