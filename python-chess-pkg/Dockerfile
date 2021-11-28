FROM python:3.8-slim

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pygame chess

COPY . /python-chess-pkg
WORKDIR /python-chess-pkg
CMD python3 main.py