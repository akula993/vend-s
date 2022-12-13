# Вытаскиваем все пакеты

> pip freeze
> pip freeze > requirements.txt

Создаем локальный репозиторий
> git init

Проверяем статус репозитория и добовляем новые
> git status
> git add . или git add -A
> git status

Создаем комит
> git commit -m "django demo and settings"

Подключаем удаленный репозиторий и пушми
> git remote add origin git@github.com:akula993/demo.git
> git push -u origin master


> git checkout master
> git checkout main

На другом компе делаем
> git clone git@github.com:akula993/demo.git


> git push origin
> git checkout main
> git checkout master
> git push origin master
>
> cd ..
> git status
> git push -u origin master

Применяем миграции
> python manage.py migrate

# DJANGO ADMIN COMMANDS

1. [ ] auth

Сбрасывает пароль
> changepassword

Создает супер узеры
> createsuperuser

2. [ ] contenttypes

> remove_stale_contenttypes

4. [ ] django

> check

> compilemessages

> createcachetable

> dbshell

Раздница в настройкай
> diffsettings

Создает Дамп базы
> dumpdata

Оистка базы данных
> flush

создание мадели по уже сушествуюшей в базе данных
> inspectdb

Используется для загрузки дампа в базу данных
> loaddata


> makemessages

Создает миграции
> makemigrations


> migrate

> optimizemigration

> sendtestemail

> shell

Просмотр миграций которые уже есть в базе данных
> showmigrations

> sqlflush

> sqlmigrate

> sqlsequencereset

Обединяет все миграции в одну
> squashmigrations

> startapp

> startproject

> test

> testserver
>

4. [ ] [sessions]

Очистка просроченых сесий
> clearsessions

5. [ ] [staticfiles]

Соберает все статические файлы
> collectstatic


> findstatic

> runserver


# vend-s
