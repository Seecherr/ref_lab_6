from django.contrib import admin
from .models import BikeModel, Order


@admin.register(BikeModel)
class BikeModelAdmin(admin.ModelAdmin):
    list_display = ("name", "bike_type", "price", "in_stock", "created_at")
    list_filter = ("bike_type", "in_stock")
    search_fields = ("name", "description")
    list_editable = ("in_stock",)
    fieldsets = (
        ("Основне", {
            "fields": ("name", "bike_type", "description", "image", "price", "in_stock")
        }),
        ("Технічні характеристики", {
            "fields": ("frame", "wheels", "brakes", "gears", "color")
        }),
        ("Електро-параметри (лише для e-bike)", {
            "classes": ("collapse",),
            "fields": ("battery_capacity", "motor_power", "range_km", "charge_time"),
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "bike", "quantity", "total_price", "status", "created_at")
    list_filter = ("status", "bike__bike_type")
    search_fields = ("user__username", "bike__name")
    list_editable = ("status",)
    readonly_fields = ("created_at", "updated_at")
