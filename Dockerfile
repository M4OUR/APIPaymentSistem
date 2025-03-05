# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app/

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# Открываем порт 8000
EXPOSE 8000

# Запуск сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
