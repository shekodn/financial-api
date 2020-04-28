# Reference: https://docs.docker.com/compose/django/

FROM python:3.7.7

ARG APP=financial_api

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

RUN mkdir /${APP}

WORKDIR /${APP}

COPY requirements.txt /${APP}/

# Install dependencies
RUN pip install -r requirements.txt

COPY . /${APP}/
