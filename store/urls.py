from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),
    path("bike/<int:pk>/", views.bike_detail, name="bike_detail"),
    path("bike/<int:pk>/order/", views.place_order, name="place_order"),
    path("order/<int:pk>/success/", views.order_success, name="order_success"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]
