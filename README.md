# Foodgram

### Алгоритм регистрации пользователей

1. Регистрация нового пользователя происходит отправлением POST-запроса с параметрами: email, username, first_name, last_name, password на эндпоинт /api/users/.
2. Авторизация нового пользователя происходит отправлением POST-запроса с параметрами: email, password на эндпоинт /api/auth/token/login/.
3. При желании пользователь может разлогиниться POST-запросом на эндпоинт /api/auth/token/logout/.

### Пользовательские роли

- Аноним — может cоздать аккаунт, просматривать рецепты на главной, просматривать отдельные страницы рецептов, просматривать страницы пользователей, фильтровать рецепты по тегам.
- Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может:
  - Создавать/редактировать/удалять собственные рецепты.
  - Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
  - Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингредиентов для рецептов из списка покупок.
  - Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.
- Администратор (admin) — полные права на управление всем контентом проекта.
- Суперюзер Django — обладает правами администратора (admin).

### Ресурсы API Foodgram

- Ресурс auth: аутентификация.
- Ресурс users: пользователи.
- Ресурс tags: теги.
- Ресурс recipes: рецепты.
- Ресурс ingredients: список ингредиентов.


### Как запустить проект локально:

- Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Unexpectedpatronus/foodgram-project-react.git
```

```
cd backend
```

- Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/bin/activate
```

- Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

- Выполнить миграции:

```
python manage.py makemigrations
```
```
python manage.py migrate
```

- Для загрузки списка ингридиентов в базу данных выполнить команду:

```
python manage.py load_data
```

- Запустить проект:

```
python manage.py runserver
```
- Открыть документацию:
```
cd ../frontend
docker compose up
```
### Документация к API с примерами запросов доступна после запуска
http://localhost/api/docs/redoc.html


### Стэк технологий:

При создании проекта использовались следующие технологии:
- Python
- Django framework
- Django-rest-framework
- Node.js
- Docker

### Об авторе:

Автор проекта: Одинцов Е.В.

ссылка на GitHub: [Unexpectedpatronus](https://github.com/Unexpectedpatronus)