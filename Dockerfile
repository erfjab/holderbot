FROM python:3.11.8-alpine

ENV TZ=Asia/Tehran \
    PYTHONUNBUFFERED=1

WORKDIR /code

RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/Asia/Tehran /etc/localtime && \
    echo "Asia/Tehran" > /etc/timezone \
    pip install --no-cache-dir --upgrade uv \
    rm -rf /var/cache/apk/*

COPY . .
RUN chmod +x main.py

CMD ["sh", "-c", "uv sync && uv run alembic upgrade head && uv run main.py"]
