FROM python:3.11.8-alpine

ENV TZ=Asia/Tehran

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN chmod +x main.py

RUN apk add --no-cache tzdata

RUN cp /usr/share/zoneinfo/Asia/Tehran /etc/localtime && echo "Asia/Tehran" > /etc/timezone

CMD ["sh", "-c", "alembic upgrade head && python3 main.py"]