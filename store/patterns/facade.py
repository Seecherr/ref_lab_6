import logging
import re
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


class ClientValidator:
    def validate(self, data: dict) -> tuple[bool, list[str]]:
        errors = []

        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")
        password_confirm = data.get("password_confirm", "")
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()

        if not username:
            errors.append("Логін не може бути порожнім.")
        elif len(username) < 3:
            errors.append("Логін має містити щонайменше 3 символи.")
        elif not re.match(r"^[a-zA-Z0-9_]+$", username):
            errors.append("Логін може містити лише латинські літери, цифри та _.")

        if not email:
            errors.append("Email не може бути порожнім.")
        elif not re.match(r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$", email):
            errors.append("Некоректний формат email.")

        if not password:
            errors.append("Пароль не може бути порожнім.")
        elif len(password) < 8:
            errors.append("Пароль має містити щонайменше 8 символів.")
        elif not re.search(r"[A-Z]", password):
            errors.append("Пароль має містити хоча б одну велику літеру.")
        elif not re.search(r"\d", password):
            errors.append("Пароль має містити хоча б одну цифру.")

        if password != password_confirm:
            errors.append("Паролі не співпадають.")

        if not first_name:
            errors.append("Ім'я не може бути порожнім.")

        if not last_name:
            errors.append("Прізвище не може бути порожнім.")

        return len(errors) == 0, errors


class ClientRepository:
    def save(self, data: dict):
        from django.contrib.auth.models import User

        user = User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        logger.info("Нового клієнта збережено: %s", user.username)
        return user


class EmailNotificationService:
    def send_confirmation(self, user) -> bool:
        subject = "✅ Вітаємо у VeloShop — реєстрацію підтверджено!"
        message = (
            f"Привіт, {user.first_name} {user.last_name}!\n\n"
            f"Ваш акаунт на VeloShop успішно створено.\n"
            f"Логін: {user.username}\n\n"
            f"Тепер ви можете замовити свій ідеальний велосипед 🚲\n\n"
            f"З повагою,\nКоманда VeloShop"
        )
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            logger.info("Лист підтвердження надіслано на: %s", user.email)
            return True
        except Exception as exc:
            logger.error("Помилка відправки листа: %s", exc)
            return False


class RegistrationFacade:
    def __init__(self):
        self._validator = ClientValidator()
        self._repository = ClientRepository()
        self._email_service = EmailNotificationService()

    def register(self, data: dict) -> tuple[bool, list[str], object | None]:
        is_valid, errors = self._validator.validate(data)
        if not is_valid:
            return False, errors, None

        from django.contrib.auth.models import User

        if User.objects.filter(username=data["username"]).exists():
            return False, ["Користувач з таким логіном вже існує."], None

        if User.objects.filter(email=data["email"]).exists():
            return False, ["Користувач з таким email вже зареєстрований."], None

        user = self._repository.save(data)

        email_sent = self._email_service.send_confirmation(user)
        if not email_sent:
            logger.warning("Реєстрацію завершено, але лист не надіслано для: %s", user.email)

        return True, [], user
