# Packaging instructions for Railway: which Python, which packages, how to start the app.
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Railway provides PORT; listen on 0.0.0.0 so it can reach the app (not localhost).
CMD gunicorn --bind 0.0.0.0:${PORT:-8080} app:app
