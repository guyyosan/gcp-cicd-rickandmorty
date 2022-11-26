# instead of:
# FROM python:3.9
# use lean image
FROM python:3.9.7-alpine3.14

# add appuser
RUN adduser --disabled-password appuser

# install required packages
RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev

WORKDIR /usr/app
ADD ./requirements.txt /usr/app/requirements.txt
RUN pip install -r requirements.txt
ADD . /usr/app
RUN chown -R appuser:appuser /usr/app

USER appuser
EXPOSE 8000
CMD gunicorn -w 1 -b 0.0.0.0:8000 server:app
