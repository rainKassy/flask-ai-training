# Используем базовый образ Python 3.10
FROM python:3.10-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем необходимые библиотеки
RUN pip install --no-cache-dir -r requirements.txt

# Указываем порт, который будет использоваться контейнером
EXPOSE 5000

# Команда для запуска Flask-сервера
CMD ["python3", "app.py"]
