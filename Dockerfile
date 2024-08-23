FROM python:3.11-slim
RUN apt-get update && apt-get install -y libpq-dev gcc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]

