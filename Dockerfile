FROM python:3.10-alpine
WORKDIR /app
ENV TZ="UTC"
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn", "-c", "hooks.py", "-b", "0.0.0.0:8000", "--workers=6", "--threads=48", "main:app"]
