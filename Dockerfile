FROM python:3.6-alpine
LABEL maintainer='Matthew Baker <m@wheres.co.uk>'

RUN adduser -D stockmon
RUN apk add curl

WORKDIR /home/stockmon

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY stockmon stockmon
COPY stockmonlib stockmonlib
COPY resources/start.sh .
RUN chmod +x start.sh

ENV FLASK_APP stockmon/app.py

RUN chown -R stockmon:stockmon .
USER stockmon

EXPOSE 5000
ENTRYPOINT ["./start.sh"]