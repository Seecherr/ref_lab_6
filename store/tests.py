from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import BikeModel, Order
from .patterns.builder import (
    ConcreteBikeBuilder,
    ConcreteElectricBikeBuilder,
    Director,
    Bike,
    ElectricBike,
)
from .patterns.facade import ClientValidator, RegistrationFacade


class BikeModelTest(TestCase):
    def setUp(self):
        self.bike = BikeModel.objects.create(
            name="Test Bike",
            bike_type="regular",
            frame="Aluminium",
            wheels="700c",
            brakes="Disc",
            gears="21 speed",
            color="Black",
            price=Decimal("15000.00"),
            in_stock=True,
        )

    def test_bike_creation(self):
        self.assertEqual(self.bike.name, "Test Bike")
        self.assertEqual(self.bike.bike_type, "regular")
        self.assertEqual(self.bike.price, Decimal("15000.00"))

    def test_bike_str(self):
        self.assertIn("Test Bike", str(self.bike))

    def test_bike_default_in_stock(self):
        bike = BikeModel.objects.create(
            name="Stock Bike",
            bike_type="regular",
            frame="Steel",
            wheels="26",
            brakes="V-brake",
            gears="7 speed",
            color="Red",
            price=Decimal("5000.00"),
        )
        self.assertTrue(bike.in_stock)

    def test_electric_bike_fields(self):
        ebike = BikeModel.objects.create(
            name="E-Bike",
            bike_type="electric",
            frame="Aluminium",
            wheels="27.5",
            brakes="Hydraulic",
            gears="10 speed",
            color="Grey",
            price=Decimal("50000.00"),
            battery_capacity="48V 14Ah",
            motor_power="750W",
            range_km=80,
            charge_time="4-5 hours",
        )
        self.assertEqual(ebike.battery_capacity, "48V 14Ah")
        self.assertEqual(ebike.range_km, 80)


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="TestPass123"
        )
        self.bike = BikeModel.objects.create(
            name="Order Bike",
            bike_type="regular",
            frame="Aluminium",
            wheels="700c",
            brakes="Disc",
            gears="21 speed",
            color="White",
            price=Decimal("10000.00"),
        )

    def test_order_auto_price(self):
        order = Order.objects.create(
            user=self.user,
            bike=self.bike,
            quantity=2,
            total_price=0,
            delivery_address="Kyiv, Ukraine",
            phone="+380991234567",
        )
        self.assertEqual(order.total_price, Decimal("20000.00"))

    def test_order_str(self):
        order = Order.objects.create(
            user=self.user,
            bike=self.bike,
            quantity=1,
            total_price=Decimal("10000.00"),
            delivery_address="Lviv",
            phone="+380991111111",
        )
        self.assertIn("testuser", str(order))
        self.assertIn("Order Bike", str(order))

    def test_order_default_status(self):
        order = Order.objects.create(
            user=self.user,
            bike=self.bike,
            quantity=1,
            total_price=Decimal("10000.00"),
            delivery_address="Odesa",
            phone="+380992222222",
        )
        self.assertEqual(order.status, "pending")


class HomePageViewTest(TestCase):
    def test_home_status_code(self):
        response = self.client.get(reverse("store:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_template(self):
        response = self.client.get(reverse("store:home"))
        self.assertTemplateUsed(response, "store/home.html")


class CatalogViewTest(TestCase):
    def setUp(self):
        BikeModel.objects.create(
            name="Regular Bike",
            bike_type="regular",
            frame="Aluminium",
            wheels="700c",
            brakes="Disc",
            gears="21 speed",
            color="Black",
            price=Decimal("15000.00"),
        )
        BikeModel.objects.create(
            name="Electric Bike",
            bike_type="electric",
            frame="Aluminium",
            wheels="27.5",
            brakes="Hydraulic",
            gears="10 speed",
            color="Grey",
            price=Decimal("50000.00"),
        )

    def test_catalog_status_code(self):
        response = self.client.get(reverse("store:catalog"))
        self.assertEqual(response.status_code, 200)

    def test_catalog_filter_regular(self):
        response = self.client.get(reverse("store:catalog") + "?type=regular")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["bikes"]), 1)

    def test_catalog_filter_electric(self):
        response = self.client.get(reverse("store:catalog") + "?type=electric")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["bikes"]), 1)

    def test_catalog_all(self):
        response = self.client.get(reverse("store:catalog") + "?type=all")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["bikes"]), 2)


class BikeDetailViewTest(TestCase):
    def setUp(self):
        self.bike = BikeModel.objects.create(
            name="Detail Bike",
            bike_type="regular",
            frame="Carbon",
            wheels="29",
            brakes="Shimano",
            gears="12 speed",
            color="Blue",
            price=Decimal("30000.00"),
        )

    def test_detail_status_code(self):
        response = self.client.get(reverse("store:bike_detail", args=[self.bike.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detail_404_for_missing(self):
        response = self.client.get(reverse("store:bike_detail", args=[9999]))
        self.assertEqual(response.status_code, 404)


class AuthViewTest(TestCase):
    def test_login_page(self):
        response = self.client.get(reverse("store:login"))
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get(reverse("store:register"))
        self.assertEqual(response.status_code, 200)

    def test_login_valid_user(self):
        User.objects.create_user(username="authuser", password="TestPass123")
        response = self.client.post(reverse("store:login"), {
            "username": "authuser",
            "password": "TestPass123",
        })
        self.assertEqual(response.status_code, 302)

    def test_login_invalid_user(self):
        response = self.client.post(reverse("store:login"), {
            "username": "nouser",
            "password": "wrong",
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        User.objects.create_user(username="logoutuser", password="TestPass123")
        self.client.login(username="logoutuser", password="TestPass123")
        response = self.client.get(reverse("store:logout"))
        self.assertEqual(response.status_code, 302)


class BuilderPatternTest(TestCase):
    def test_regular_bike_builder(self):
        builder = ConcreteBikeBuilder()
        director = Director(builder)
        bike = director.create_order(
            frame="Aluminium",
            wheels="700c",
            brakes="Disc",
            gears="21 speed",
            color="Black",
            price=15000.0,
        )
        self.assertIsInstance(bike, Bike)
        self.assertEqual(bike.bike_type, "regular")
        self.assertEqual(bike.frame, "Aluminium")
        self.assertEqual(bike.price, 15000.0)

    def test_electric_bike_builder(self):
        builder = ConcreteElectricBikeBuilder()
        director = Director(builder)
        bike = director.create_order(
            frame="Carbon",
            wheels="29",
            brakes="Shimano",
            gears="12 speed",
            color="Grey",
            price=50000.0,
            battery="48V 14Ah",
            motor="750W",
            range_km=80,
            charge_time="4-5 hours",
        )
        self.assertIsInstance(bike, ElectricBike)
        self.assertEqual(bike.bike_type, "electric")
        self.assertEqual(bike.battery_capacity, "48V 14Ah")
        self.assertEqual(bike.range_km, 80)

    def test_builder_reset_after_build(self):
        builder = ConcreteBikeBuilder()
        builder.set_frame("Frame1").set_price(1000.0)
        bike1 = builder.build()
        bike2 = builder.build()
        self.assertEqual(bike1.frame, "Frame1")
        self.assertEqual(bike2.frame, "")


class FacadePatternTest(TestCase):
    def test_validator_empty_username(self):
        validator = ClientValidator()
        is_valid, errors = validator.validate({
            "username": "",
            "email": "test@test.com",
            "password": "TestPass1",
            "password_confirm": "TestPass1",
            "first_name": "Test",
            "last_name": "User",
        })
        self.assertFalse(is_valid)
        self.assertTrue(any("Логін" in e for e in errors))

    def test_validator_short_password(self):
        validator = ClientValidator()
        is_valid, errors = validator.validate({
            "username": "testuser",
            "email": "test@test.com",
            "password": "short",
            "password_confirm": "short",
            "first_name": "Test",
            "last_name": "User",
        })
        self.assertFalse(is_valid)

    def test_validator_password_mismatch(self):
        validator = ClientValidator()
        is_valid, errors = validator.validate({
            "username": "testuser",
            "email": "test@test.com",
            "password": "TestPass1",
            "password_confirm": "DifferentPass1",
            "first_name": "Test",
            "last_name": "User",
        })
        self.assertFalse(is_valid)

    def test_facade_successful_registration(self):
        facade = RegistrationFacade()
        success, errors, user = facade.register({
            "username": "newuser",
            "email": "new@test.com",
            "password": "TestPass1",
            "password_confirm": "TestPass1",
            "first_name": "New",
            "last_name": "User",
        })
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "newuser")

    def test_facade_duplicate_username(self):
        User.objects.create_user(username="existing", password="TestPass1")
        facade = RegistrationFacade()
        success, errors, user = facade.register({
            "username": "existing",
            "email": "new2@test.com",
            "password": "TestPass1",
            "password_confirm": "TestPass1",
            "first_name": "Dup",
            "last_name": "User",
        })
        self.assertFalse(success)
        self.assertIsNone(user)
