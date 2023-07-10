FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install -U pip &&\
    pip install -r requirements.txt --no-cache-dir

RUN chmod +x run_app.sh
ENTRYPOINT ["/app/run_app.sh"]