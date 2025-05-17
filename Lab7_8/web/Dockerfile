FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY hospital .

# Устанавливаем переменную окружения для Django
ENV DJANGO_SETTINGS_MODULE=hospital.settings

EXPOSE 8000

# Запускаем Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "hospital.wsgi:application"]