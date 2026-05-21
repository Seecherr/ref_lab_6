# 🚲 VeloShop — Інтернет-магазин велосипедів

![CI/CD](https://github.com/<username>/veloshop/actions/workflows/ci.yml/badge.svg)

Django-додаток для продажу звичайних та електровелосипедів з каталогом, системою замовлень, реєстрацією користувачів та адмін-панеллю.

## Технології

| Компонент        | Технологія                |
|------------------|---------------------------|
| Backend          | Django 6.0 (Python 3.12)  |
| База даних       | PostgreSQL 16 / SQLite    |
| Production сервер| Gunicorn                  |
| Контейнеризація  | Docker, Docker Compose    |
| CI/CD            | GitHub Actions            |
| Лінтер           | flake8                    |

## Запуск через Docker

### Передумови
- Docker та Docker Compose встановлені на системі

### Кроки

```bash
# 1. Клонувати репозиторій
git clone https://github.com/<username>/veloshop.git
cd veloshop

# 2. Запустити додаток та базу даних
docker-compose up --build

# 3. Відкрити у браузері
# http://localhost:8000
```

Команда `docker-compose up` автоматично:
- Піднімає контейнер PostgreSQL
- Застосовує міграції (`migrate`)
- Заповнює каталог демо-даними (`seed_bikes`)
- Запускає Gunicorn на порту 8000

### Зупинити

```bash
docker-compose down
```

### Видалити дані БД

```bash
docker-compose down -v
```

## Локальний запуск (без Docker)

```bash
# 1. Створити віртуальне оточення
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Встановити залежності
pip install -r requirements.txt

# 3. Застосувати міграції
python manage.py migrate

# 4. Заповнити каталог демо-даними
python manage.py seed_bikes

# 5. Створити суперкористувача (для адмін-панелі)
python manage.py createsuperuser

# 6. Запустити сервер розробки
python manage.py runserver
```

Додаток буде доступний за адресою `http://127.0.0.1:8000`

## Змінні середовища

| Змінна                 | Опис                                    | За замовчуванням              |
|------------------------|-----------------------------------------|-------------------------------|
| `DJANGO_SECRET_KEY`    | Секретний ключ Django                   | insecure ключ для розробки    |
| `DJANGO_DEBUG`         | Режим налагодження (True/False)         | `True`                        |
| `DJANGO_ALLOWED_HOSTS` | Дозволені хости (через кому)            | `localhost,127.0.0.1`         |
| `DB_ENGINE`            | Двигун БД: `sqlite3` або `postgresql`   | `sqlite3`                     |
| `DB_NAME`              | Назва бази даних                        | `veloshop`                    |
| `DB_USER`              | Користувач БД                           | `veloshop`                    |
| `DB_PASSWORD`          | Пароль БД                               | `veloshop`                    |
| `DB_HOST`              | Хост БД                                 | `db`                          |
| `DB_PORT`              | Порт БД                                 | `5432`                        |

## Основні сторінки / ендпоінти

| URL                        | Метод  | Опис                              |
|----------------------------|--------|-----------------------------------|
| `/`                        | GET    | Головна сторінка                  |
| `/catalog/`                | GET    | Каталог велосипедів               |
| `/catalog/?type=regular`   | GET    | Фільтр: звичайні велосипеди       |
| `/catalog/?type=electric`  | GET    | Фільтр: електровелосипеди         |
| `/bike/<id>/`              | GET    | Деталі велосипеда                 |
| `/bike/<id>/order/`        | GET/POST | Оформлення замовлення           |
| `/order/<id>/success/`     | GET    | Підтвердження замовлення          |
| `/my-orders/`              | GET    | Мої замовлення (потрібен логін)   |
| `/register/`               | GET/POST | Реєстрація нового користувача   |
| `/login/`                  | GET/POST | Вхід до системи                 |
| `/logout/`                 | GET    | Вихід із системи                  |
| `/admin/`                  | GET    | Адміністративна панель Django     |

## Тести

### Запуск тестів локально

```bash
python manage.py test --verbosity=2
```

### Запуск тестів через Docker

```bash
docker-compose --profile test run test
```

### Що тестується

| Категорія          | Тести                                              |
|--------------------|-----------------------------------------------------|
| Моделі             | Створення BikeModel, автоматична ціна Order          |
| В'юхи (Views)      | Статус-коди сторінок, фільтрація каталогу, 404       |
| Аутентифікація      | Реєстрація, вхід, вихід, невірний логін             |
| Builder Pattern    | Створення regular/electric, скидання після build      |
| Facade Pattern     | Валідація даних, успішна реєстрація, дублювання       |

### Очікуваний результат

Усі тести повинні пройти успішно:

```
Ran XX tests in X.XXXs

OK
```

## Як перевірити роботу

1. Запустити додаток (через Docker або локально)
2. Відкрити `http://localhost:8000` у браузері
3. Перевірити головну сторінку — повинні відображатися велосипеди
4. Перейти до каталогу — перевірити фільтрацію за типом
5. Зареєструвати нового користувача
6. Оформити замовлення на велосипед
7. Перевірити "Мої замовлення"
8. Зайти в адмін-панель `/admin/` (потрібен суперкористувач)

## CI/CD Pipeline

Конвеєр GitHub Actions виконує три етапи:

1. **Lint** — статичний аналіз коду за допомогою flake8
2. **Test** — запуск юніт- та інтеграційних тестів
3. **Docker Build** — збірка Docker-образу для перевірки Dockerfile

Конвеєр запускається автоматично при кожному push або pull request до гілок `main` / `master`.

## Структура проєкту

```
veloshop/
├── bike_shop/               # Налаштування Django проєкту
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── store/                   # Головний додаток магазину
│   ├── models.py            # BikeModel, Order
│   ├── views.py             # Обробники запитів
│   ├── urls.py              # Маршрути додатку
│   ├── admin.py             # Адмін-панель
│   ├── tests.py             # Тести
│   ├── templates/store/     # HTML-шаблони
│   ├── patterns/
│   │   ├── builder.py       # Builder pattern
│   │   └── facade.py        # Facade pattern
│   └── management/commands/
│       └── seed_bikes.py    # Команда для заповнення каталогу
├── static/css/              # Статичні файли (CSS)
├── Dockerfile               # Образ Docker
├── docker-compose.yaml      # Багатосервісна конфігурація
├── .github/workflows/ci.yml # CI/CD конвеєр
├── requirements.txt         # Python залежності
└── README.md                # Документація
```
