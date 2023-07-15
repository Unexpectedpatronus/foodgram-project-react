![<-foodgram workflow](https://github.com/unexpectedpatronus/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# Foodgram
## Описание проекта
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Технологии
[![Python](https://img.shields.io/badge/Python-gray?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-gray?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![DjangoREST](https://img.shields.io/badge/Django-REST-gray?style=flat-square&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-gray?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![Postgres](https://img.shields.io/badge/Postgres-gray?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-gray?style=flat-square&logo=docker)](https://www.docker.com/)
[![Nginx](https://img.shields.io/badge/Nginx-gray?style=flat-square&logo=nginx)](https://www.nginx.org/)


###  Запуск проекта в Docker
- Необходимо склонировать репозиторий с проектом:

```
git clone git@github.com:гтучзусеувзфекщтгы/foodgram-project-react.git
```

- В корневой директории необходимо создать файл .env, содержащий переменные окружения 
  - Пример заполнения файла .env:

```
SECRET_KEY=Секретный_ключ
DEBUG=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

- Запустить проект в Docker-контейнерах:

```
cd infra
docker-compose up -d --build
```

- Будут созданы и запущены в фоновом режиме необходимые для работы приложения контейнеры: db, backend, nginx (а так же запущен и остановлен контейнер frontend, который необходим для раздачи статики). Внутри контейнера backend необходимо выполнить миграции, создать суперпользователя и собрать статику:

```
docker-compose exec backend python manage.py migrate --no-input
docker-compose exec backend python manage.py collectstatic --no-input
docker compose exec -T backend cp -r /app/static/. /backend_static/
docker-compose exec backend python manage.py createsuperuser
```

### Запуск проекта локально

- Необходимо склонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Unexpectedpatronus/foodgram-project-react.git
```

```
cd backend
```

- Cоздать и активировать виртуальное окружение:

```
python -m venv venv
source venv/bin/activate
```

- Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- Выполнить миграции:

```
python manage.py makemigrations
python manage.py migrate
```

- Для загрузки списка ингридиентов в базу данных необходимо выполнить команду:

```
python manage.py load_data
```

- Для загрузки тегов в базу данных необходимо выполнить команду:

```
python manage.py load_tags
```

- Запустить проект:

```
python manage.py runserver
```
- Открыть документацию:
```
cd ../infra
docker compose up
```
### Документация к API с примерами запросов доступна после запуска:
http://localhost/api/docs/redoc.html

### Об авторе:

Автор проекта: Одинцов Е.В.

ссылка на GitHub: [Unexpectedpatronus](https://github.com/Unexpectedpatronus)