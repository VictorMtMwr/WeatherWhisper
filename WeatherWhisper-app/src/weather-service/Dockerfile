FROM python:3.12.7-alpine  

RUN apk add --no-cache \
    build-base \
    postgresql-dev \
    libffi-dev \
    openssl-dev

RUN pip install --upgrade pip

WORKDIR /app

COPY . .

EXPOSE 5001

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
