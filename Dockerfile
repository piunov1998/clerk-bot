FROM python:3.10-slim

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt && rm requirements.txt

COPY . /app

WORKDIR /app/src

CMD python3 bot_runner.py