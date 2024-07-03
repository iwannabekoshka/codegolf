# Используем официальный образ Python в качестве базового
FROM python:3.9

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /code

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt /code/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию, исключая файлы, указанные в .dockerignore
COPY . /code/

# Указываем команду по умолчанию для запуска сервера разработки Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]