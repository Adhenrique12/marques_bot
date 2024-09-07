FROM python:3.12-bookworm

ENV PYTHONBUFFERED=1

WORKDIR /mackiabot

# Instalar FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD python main.py