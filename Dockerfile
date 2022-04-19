FROM python:3.9-alpine

WORKDIR /app

COPY poll_bot /app/poll_bot
COPY requirements.txt /app

RUN pip3 install -r requirements.txt

ENV PYTHONPATH /app

RUN adduser galactic-poll -G nobody -u 2000 -D -H
#RUN chown -R galactic-poll:galactic-poll /app
USER galactic-poll:nobody

EXPOSE 80
CMD ["gunicorn", "--workers=1", "--threads=4","--bind=0.0.0.0:80", "poll_bot.main"]
