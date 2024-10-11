FROM python:3.11.8-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN pip install alembic

COPY . .

RUN alembic upgrade head

RUN chmod +x main.py

CMD [ "python3", "main.py" ]
