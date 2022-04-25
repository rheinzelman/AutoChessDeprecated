FROM python:3.9

WORKDIR /usr/src/autochessdeprecated

COPY . .

RUN pip install pygame

RUN pip install chess

CMD ["python3", "windows/game.py"]

