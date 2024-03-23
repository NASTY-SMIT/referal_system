# RESTful API сервис для реферальной системы

# В проекте реализовано:
- регистрация и аутентификация пользователя (JWT, Djoser);
- аутентифицированный пользователь имеет возможность создать или удалить свой реферальный код. (Одновременно может быть активен только 1 код), также при создании кода всегда указывается его срок годности;
- возможность получения реферального кода по email адресу реферера;
- возможность регистрации по реферальному коду в качестве реферала;	
- получение информации о рефералах по id реферера;

## Описание:
- Проект написан по стандарту PEP8, использовался линтинг flake8.
- Все  I/O bound операции с реферальными кодами являются ассинхронными.
- При создании и получении реферального кода используется кеширование с использованием in-memory БД (django.core.cache).
- Написана документация Redoc ко всем запросам API.

## Используемый стек

[![Python][Python-badge]][Python-url]
[![Django][Django-badge]][Django-url]
[![DRF][DRF-badge]][DRF-url]

## Архитектура проекта

| Директория       | Описание                                                |
|---------------   |---------------------------------------------------------|
| `referal_system` | Код Django приложения                                   |
| `docs`           | Документация Redoc                                      |

# Подготовка

## Требования

1. **Python 3.10**  
   Убедитесь, что у вас установлена нужная версия Python или активирована в
   `pyenv`.

2. **Poetry**  
   Зависимости и пакеты управляются через poetry. Убедитесь, что poetry [установлен](https://python-poetry.org/docs/#installing-with-the-official-installer)
   на вашем компьютере и ознакомьтесь с [документацией](https://python-poetry.org/docs/basic-usage/).  
   Установка зависимостей из корневой дирректории проекта

   ```
   poetry install
   ```

   Также будет создано виртуальное окружение, если привычнее видеть его в
   директории проекта, то
   используйте [настройку](https://python-poetry.org/docs/configuration/#adding-or-updating-a-configuration-setting) `virtualenvs.in-project`

# Разворачиваем проект локально

1. Устанавливаем зависимости
  ```
   poetry install
   ```
2. Активируем виртуальное окружение
  ```
   poetry shell
   ```

3. Создаём `.env` файл в корневой директории проекта и заполняем его по
образцу `.env.example`

4. Переходим в директорию `referal_system`
   ```shell
   cd referal_system
   ```

4. Применяем миграции
   ```shell
   python manage.py migrate
   ```

6. Запускаем *development*-сервер *Django*
   ```shell
   python manage.py runserver
   ```

7. Открываем [документацию Redoc](https://redocly.github.io/redoc/) и загружаем туда файл с документацией API из папки docs

### Пример использования: (тело запросов необходимо взять из документации)

1. Необходимо зарегестрировать пользователя в качестве реферера.
- Отправляем запрос по адресу POST http://127.0.0.1:8000/auth/users/

2. Получаем JWT токен по адресу POST  http://127.0.0.1:8000/auth/token/login/
- Далее если вы тестируете проект с помощью Postmen необходимо на вкладке Authorisation выбрать type API Key, в поле key прописать "Authorization", а в поле value прописать "Token <ваш токен>". Далее все запросы будут идти от авторизованного пользователя.

3. Создаем реферальный код.
- Отправляем запрос по адресу POST http://127.0.0.1:8000/api/referral_codes/create/
- Указываем срок годности (обязательно позже сегодняшней даты) и в ответ придет сгенерированный реферальный код, который будет закреплен за данным пользователем.

##### С остальными эндпоинтами можно ознакомиться в документации из шага 7 по развертыванию проекта.

❤️Автор [Nasty Shmidt](https://github.com/NASTY-SMIT)❤️
[Обратная связь](https://t.me/nastyShmidt) - Telegram

[Python-url]: https://www.python.org/

[Python-badge]: https://img.shields.io/badge/Python-376f9f?style=for-the-badge&logo=python&logoColor=white

[Django-url]: https://github.com/django/django

[Django-badge]: https://img.shields.io/badge/Django-0c4b33?style=for-the-badge&logo=django&logoColor=white

[DRF-url]: https://github.com/encode/django-rest-framework

[DRF-badge]: https://img.shields.io/badge/DRF-a30000?style=for-the-badge
