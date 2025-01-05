FROM python:3.11.8-alpine

ENV TZ=Asia/Tehran \
    PYTHONUNBUFFERED=1

RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/Asia/Tehran /etc/localtime && \
    echo "Asia/Tehran" > /etc/timezone

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .
RUN chmod +x main.py

CMD ["sh", "-c", "alembic upgrade head && python3 main.py"]