FROM python:3.9
WORKDIR /usr/src/AutoChessDeprecated/windows

COPY . .

RUN pip install pygame

RUN pip install chess

CMD ["python3", "game.py"]