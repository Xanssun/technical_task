FROM python:3.11.5

WORKDIR /app

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt update && apt install netcat-traditional

COPY schedule/ .

ENTRYPOINT ["sh", "entrypoint.sh"]
