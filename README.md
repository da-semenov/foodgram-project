![foodgram](https://github.com/da-semenov/foodgram-project/workflows/foodgram_workflow.yaml/badge.svg?branch=master)

[![Python](https://img.shields.io/badge/-Python-464646??style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646??style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646??style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![NGINX](https://img.shields.io/badge/-NGINX-464646??style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![docker](https://img.shields.io/badge/-Docker-464646??style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646??style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

# Foodgram-project
## 
Приложение «Продуктовый помощник»: сайт, на котором пользователи будут публиковать
рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов.
Сервис «Список покупок» позволит пользователям создавать список продуктов, 
которые нужно купить для приготовления выбранных блюд и скачать его в формате pdf.

### Адрес сайта
http://178.154.193.199

---
Для проекта настроен Continuous Integration и Continuous Deployment:
автоматический запуск тестов, обновление образов на Docker Hub и автоматический деплой
на боевой сервер при пуше в ветку main.

---

## Технические требования и инфраструктура </h3>

- Проект использует базу данных PostgreSQL.
- Проект запускается в трёх контейнерах (Nginx, PostgreSQL и Django)

## Необходимое ПО

Docker: https://www.docker.com/get-started <br />
Docker-compose: https://docs.docker.com/compose/install/


## Установка

#### 1. Клонируйте репозиторий на локальную машину
```bash
git clone https://github.com/da-semenov/foodgram-project
```

#### 2. В корневой папке проекта на сервере необходимо создать файл ```.env``` с данными для подключения к базе данных ```postgresql```.
В репозитории есть образец .env.example


#### 3. Добавьте Action secrets в репозитории на GitHub в разделе settings -> Secrets:
* HOST - ip-адрес сервера
* USER - имя пользователя для подключения к серверу
* SSH_KEY - приватный ssh ключ
* PASSPHRASE - если при создании ssh-ключа вы использовали фразу-пароль, то добавьте также переменную
* DOCKER_USERNAME - логин DockerHub
* DOCKER_PASSWORD - пароль DockerHub
* TELEGRAM_TO - id вашего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
* TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)


#### 4. После выполнения push необходимо зайти на сервер
```bash
$ ssh username@server_address
```

#### 5. Отобразить список работающих контейнеров
```bash
$ sudo docker container ls
```

#### 6. Зайти в контейнер foodgram-project по id контейнера
```bash
$ sudo docker exec -it 123456789012 bash
```

#### 7. Выполнить миграции внутри этого контейнера
```bash
python manage.py migrate
```

#### 8. Собрать статику
```bash
python manage.py collectstatic
```

#### 9. Создайте суперпользователя для работы с админкой ```Django```
```bash
python manage.py createsuperuser
```

#### 10. Выгрузите данные из файла csv с ингредиентами
```bash
python manage.py import_csv
```

#### 11. При желании можно загрузить тестовую базу
```bash
python manage.py loaddata dump.json
```


## Основные использованные технологии
* [python 3.8](https://www.python.org/)
* [django](https://www.djangoproject.com/)
* [drf](https://www.django-rest-framework.org/)
* [posgresql](https://www.postgresql.org/)
* [docker](https://www.docker.com/)
* [nginx](https://nginx.org/)

## Автор

* **Семенов Денис** - [da-semenov](https://github.com/da-semenov)
* **Сайт:** http://178.154.193.199
