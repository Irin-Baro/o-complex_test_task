[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)


# o-complex_test_task
Тестовое задание от "О-комплекс" на позицию "Junior Python разработчик"

- [Описание](#description)
- [Установка](#run)
- [Запуск](#docker)
- [Автор](#author)


## Описание <a id=description></a>

Проект предоставляет пользователям следующие возможности:
- узнавать погоду в любом городе по местному времени
- регистрироваться в приложении (добавлена функция смены пароля)
- после авторизации доступна история своих запросов
- при повторном посещении сайта предложено посмотреть погоду в последнем запрашиваемом городе
- реализована функция api, позволяющая узнать какие города и сколько раз запрашивали на сайте. Запрос доступен при запущенном приложении по адресу: [http://127.0.0.1:8000/api/v1/city-search-count/](http://127.0.0.1:8000/api/v1/city-search-count/)
- в проекте написаны тесты
- приложение помещено в Docker-контейнер

При запуске проект доступен по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Установка <a id=run></a>

1. Клонируйте репозиторий:

    ```sh
    git clone https://github.com/Irin-Baro/o-complex_test_task
    ```
    ```sh
    cd o-complex_test_task
    ```
2. Создайте файл .env и заполните его своими данными. (Пример в корневой директории проекта в файле .env.example)

### Создание Docker-образов и запуск проекта <a id=docker></a>

3. Запуск проекта:

    ```sh
    docker-compose up --build
    ```

## Автор <a id=author></a>
 
- [Ирина Баронская](https://t.me/irin_baro)