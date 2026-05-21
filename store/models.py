from django.db import models
from django.contrib.auth.models import User


class BikeModel(models.Model):
    BIKE_TYPE_CHOICES = [
        ("regular", "Звичайний велосипед"),
        ("electric", "Електровелосипед"),
    ]

    name = models.CharField("Назва", max_length=120)
    bike_type = models.CharField(
        "Тип велосипеда",
        max_length=10,
        choices=BIKE_TYPE_CHOICES,
        default="regular",
    )
    frame = models.CharField("Рама", max_length=100)
    wheels = models.CharField("Колеса", max_length=100)
    brakes = models.CharField("Гальма", max_length=100)
    gears = models.CharField("Передачі", max_length=100)
    color = models.CharField("Колір", max_length=60)
    price = models.DecimalField("Ціна (грн)", max_digits=10, decimal_places=2)
    image = models.ImageField("Зображення", upload_to="bikes/", blank=True, null=True)
    description = models.TextField("Опис", blank=True)

    battery_capacity = models.CharField("Акумулятор", max_length=80, blank=True)
    motor_power = models.CharField("Мотор", max_length=80, blank=True)
    range_km = models.PositiveIntegerField("Запас ходу (км)", default=0)
    charge_time = models.CharField("Час заряджання", max_length=60, blank=True)

    in_stock = models.BooleanField("В наявності", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Велосипед"
        verbose_name_plural = "Велосипеди"
        ordering = ["bike_type", "price"]

    def __str__(self):
        return f"{self.name} ({self.get_bike_type_display()})"


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Очікує обробки"),
        ("confirmed", "Підтверджено"),
        ("shipped", "Відправлено"),
        ("delivered", "Доставлено"),
        ("cancelled", "Скасовано"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Клієнт",
    )
    bike = models.ForeignKey(
        BikeModel,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Велосипед",
    )
    quantity = models.PositiveIntegerField("Кількість", default=1)
    total_price = models.DecimalField("Загальна вартість", max_digits=12, decimal_places=2)
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    delivery_address = models.TextField("Адреса доставки")
    phone = models.CharField("Телефон", max_length=20)
    comment = models.TextField("Коментар", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Замовлення #{self.pk} — {self.user.username} — {self.bike.name}"

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.bike.price * self.quantity
        super().save(*args, **kwargs)
