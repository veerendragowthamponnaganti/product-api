FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

ENV APP_ENV=production
ENV DB_HOST=localhost
ENV APP_PORT=8080

EXPOSE 8080

CMD ["python", "app.py"]