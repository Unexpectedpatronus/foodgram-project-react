FROM python:3.10.11-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi"]