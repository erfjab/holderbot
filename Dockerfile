FROM python:3.11.8-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN chmod +x main.py

CMD ["sh", "-c", "alembic upgrade head && python3 main.py"]