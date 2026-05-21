from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import BikeModel, Order
from .patterns.builder import (
    Director,
    ConcreteBikeBuilder,
    ConcreteElectricBikeBuilder,
)
from .patterns.facade import RegistrationFacade


def home(request):
    regular_bikes = BikeModel.objects.filter(bike_type="regular", in_stock=True)[:3]
    electric_bikes = BikeModel.objects.filter(bike_type="electric", in_stock=True)[:3]
    return render(request, "store/home.html", {
        "regular_bikes": regular_bikes,
        "electric_bikes": electric_bikes,
    })


def catalog(request):
    bike_type = request.GET.get("type", "all")

    if bike_type == "regular":
        bikes = BikeModel.objects.filter(bike_type="regular", in_stock=True)
    elif bike_type == "electric":
        bikes = BikeModel.objects.filter(bike_type="electric", in_stock=True)
    else:
        bikes = BikeModel.objects.filter(in_stock=True)

    return render(request, "store/catalog.html", {
        "bikes": bikes,
        "selected_type": bike_type,
    })


def bike_detail(request, pk):
    bike = get_object_or_404(BikeModel, pk=pk, in_stock=True)
    return render(request, "store/bike_detail.html", {"bike": bike})


def register(request):
    if request.user.is_authenticated:
        return redirect("store:home")

    if request.method == "POST":
        facade = RegistrationFacade()
        data = {
            "username": request.POST.get("username", ""),
            "email": request.POST.get("email", ""),
            "password": request.POST.get("password", ""),
            "password_confirm": request.POST.get("password_confirm", ""),
            "first_name": request.POST.get("first_name", ""),
            "last_name": request.POST.get("last_name", ""),
        }

        success, errors, user = facade.register(data)

        if success:
            login(request, user)
            messages.success(
                request,
                f"Вітаємо, {user.first_name}! Реєстрацію успішно завершено. "
                f"Лист підтвердження надіслано на {user.email}."
            )
            return redirect("store:home")
        else:
            for error in errors:
                messages.error(request, error)
            return render(request, "store/register.html", {"form_data": data, "errors": errors})

    return render(request, "store/register.html")


def user_login(request):
    if request.user.is_authenticated:
        return redirect("store:home")

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"З поверненням, {user.first_name}!")
            return redirect("store:home")
        else:
            messages.error(request, "Невірний логін або пароль.")

    return render(request, "store/login.html")


def user_logout(request):
    logout(request)
    messages.info(request, "Ви вийшли з акаунту.")
    return redirect("store:home")


@login_required
def place_order(request, pk):
    bike_db = get_object_or_404(BikeModel, pk=pk, in_stock=True)

    if request.method == "POST":
        if bike_db.bike_type == "electric":
            builder = ConcreteElectricBikeBuilder()
        else:
            builder = ConcreteBikeBuilder()

        director = Director(builder)

        bike_product = director.create_order(
            frame=bike_db.frame,
            wheels=bike_db.wheels,
            brakes=bike_db.brakes,
            gears=bike_db.gears,
            color=bike_db.color,
            price=float(bike_db.price),
            battery=bike_db.battery_capacity,
            motor=bike_db.motor_power,
            range_km=bike_db.range_km,
            charge_time=bike_db.charge_time,
        )

        quantity = int(request.POST.get("quantity", 1))
        delivery_address = request.POST.get("delivery_address", "")
        phone = request.POST.get("phone", "")
        comment = request.POST.get("comment", "")

        if not delivery_address or not phone:
            messages.error(request, "Будь ласка, вкажіть адресу доставки та телефон.")
            return render(request, "store/order.html", {"bike": bike_db})

        order = Order.objects.create(
            user=request.user,
            bike=bike_db,
            quantity=quantity,
            total_price=bike_product.price * quantity,
            delivery_address=delivery_address,
            phone=phone,
            comment=comment,
        )

        messages.success(
            request,
            f"Замовлення #{order.pk} успішно оформлено! "
            f"Очікуйте підтвердження від менеджера."
        )
        return redirect("store:order_success", pk=order.pk)

    return render(request, "store/order.html", {"bike": bike_db})


@login_required
def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "store/order_success.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).select_related("bike")
    return render(request, "store/my_orders.html", {"orders": orders})
