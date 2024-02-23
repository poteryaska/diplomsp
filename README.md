# Django simple referral system

## Пример реферальной системы на Django (авторизация по номеру телефона, с отправкой 4-х значного кода авторизации)

### Установка
#### При локальном запуске
* Клонируете проект в свою директорию
https://github.com/poteryaska/diplomsp.git
* Создаете виртуальное окружение python3 -m venv venv
* Активируйте виртуальное окружение source venv/bin/activate
* Устанавливаете зависимости pip3 install -r requirements.txt
* Создайте файл .env по примеру файла .env.example
* Создайте БД в postgres
* Создайте миграции python3 manage.py makemigrations
* Применяете миграции python3 manage.py migrate
* Запускаете команду python manage.py runserver

#### При запуске через Docker
* Создайте файл .env по примеру файла .env.example
* Запускаете команду docker compose up --build

### Работа с API
* POST запрос на регистацию пользователя http://127.0.0.1:8000/registration/
#### {
    "phone": "+79213647575"
#### }
* POST запрос для ввода 4х значного кода http://127.0.0.1:8000/authorization/
#### {
     "phone": "Maks",
     "code": "6179"
#### }
* PATCH запрос для ввода чужого инвайт-кода http://127.0.0.1:8000/user/12/
#### {
     "else_referral_code": "xx7yb5"
#### }
* GET запрос на просмотр профиля пользователя http://127.0.0.1:8000/user/12/ Получаем данные пользователся с именами и телефонами пользователей, которые воспользовались инвайт-кодом текущего пользователя
#### {
        "username": "Maks",
        "phone": "+79213647575",
        "referral_code": "ekvdbp",
        "else_referral_code": xx7yb5,
        "activated": true
    },
    [
        {
            "username": "Katya",
            "phone": "+79213647778"
        },
        {
            "username": "Masha",
            "phone": "+79213647772"
        },
        {
            "username": "Mars",
            "phone": "+79213647775"
        },
        {
            "username": "Maks",
            "phone": "+79213647575"
        }
    ]
#### 