# syntax=docker/dockerfile:1.0.0-experimental
FROM python:3.8.2-slim-buster

RUN pip install seqtolang transformers sentencepiece pymysql

COPY app.py app.py

ENTRYPOINT ["python", "app.py"]
