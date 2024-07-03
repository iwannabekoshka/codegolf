# Используем официальный образ Python в качестве базового
FROM nikolaik/python-nodejs:python3.12-nodejs22

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /code

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt /code/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию, исключая файлы, указанные в .dockerignore
COPY . /code/

# Устанавливаем зависимости и строим статику для фронтенда
WORKDIR /code/src
RUN npm install && npm run build

# Возвращаемся в рабочую директорию проекта
WORKDIR /code

# Указываем команду по умолчанию для запуска сервера разработки Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8100"]