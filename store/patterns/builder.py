from abc import ABC, abstractmethod


class Product:
    def __init__(self):
        self.frame: str = ""
        self.wheels: str = ""
        self.brakes: str = ""
        self.gears: str = ""
        self.color: str = ""
        self.price: float = 0.0
        self.bike_type: str = ""

    def get_specs(self) -> dict:
        return {
            "Тип": self.bike_type,
            "Рама": self.frame,
            "Колеса": self.wheels,
            "Гальма": self.brakes,
            "Передачі": self.gears,
            "Колір": self.color,
            "Ціна": f"{self.price:.2f} грн",
        }

    def __str__(self) -> str:
        specs = self.get_specs()
        return "\n".join(f"  {k}: {v}" for k, v in specs.items())


class Bike(Product):
    def __init__(self):
        super().__init__()
        self.bike_type = "regular"


class ElectricBike(Product):
    def __init__(self):
        super().__init__()
        self.bike_type = "electric"
        self.battery_capacity: str = ""
        self.motor_power: str = ""
        self.range_km: int = 0
        self.charge_time: str = ""

    def get_specs(self) -> dict:
        specs = super().get_specs()
        specs.update({
            "Акумулятор": self.battery_capacity,
            "Мотор": self.motor_power,
            "Запас ходу": f"{self.range_km} км",
            "Час заряджання": self.charge_time,
        })
        return specs


class BikeBuilder(ABC):
    @abstractmethod
    def set_frame(self, frame: str) -> "BikeBuilder":
        pass

    @abstractmethod
    def set_wheels(self, wheels: str) -> "BikeBuilder":
        pass

    @abstractmethod
    def set_brakes(self, brakes: str) -> "BikeBuilder":
        pass

    @abstractmethod
    def set_gears(self, gears: str) -> "BikeBuilder":
        pass

    @abstractmethod
    def set_color(self, color: str) -> "BikeBuilder":
        pass

    @abstractmethod
    def set_price(self, price: float) -> "BikeBuilder":
        pass

    @abstractmethod
    def build(self) -> Product:
        pass


class ConcreteBikeBuilder(BikeBuilder):
    def __init__(self):
        self._bike = Bike()

    def set_frame(self, frame: str) -> "ConcreteBikeBuilder":
        self._bike.frame = frame
        return self

    def set_wheels(self, wheels: str) -> "ConcreteBikeBuilder":
        self._bike.wheels = wheels
        return self

    def set_brakes(self, brakes: str) -> "ConcreteBikeBuilder":
        self._bike.brakes = brakes
        return self

    def set_gears(self, gears: str) -> "ConcreteBikeBuilder":
        self._bike.gears = gears
        return self

    def set_color(self, color: str) -> "ConcreteBikeBuilder":
        self._bike.color = color
        return self

    def set_price(self, price: float) -> "ConcreteBikeBuilder":
        self._bike.price = price
        return self

    def build(self) -> Bike:
        result = self._bike
        self._bike = Bike()
        return result


class ConcreteElectricBikeBuilder(BikeBuilder):
    def __init__(self):
        self._bike = ElectricBike()

    def set_frame(self, frame: str) -> "ConcreteElectricBikeBuilder":
        self._bike.frame = frame
        return self

    def set_wheels(self, wheels: str) -> "ConcreteElectricBikeBuilder":
        self._bike.wheels = wheels
        return self

    def set_brakes(self, brakes: str) -> "ConcreteElectricBikeBuilder":
        self._bike.brakes = brakes
        return self

    def set_gears(self, gears: str) -> "ConcreteElectricBikeBuilder":
        self._bike.gears = gears
        return self

    def set_color(self, color: str) -> "ConcreteElectricBikeBuilder":
        self._bike.color = color
        return self

    def set_price(self, price: float) -> "ConcreteElectricBikeBuilder":
        self._bike.price = price
        return self

    def set_battery(self, capacity: str) -> "ConcreteElectricBikeBuilder":
        self._bike.battery_capacity = capacity
        return self

    def set_motor(self, power: str) -> "ConcreteElectricBikeBuilder":
        self._bike.motor_power = power
        return self

    def set_range(self, km: int) -> "ConcreteElectricBikeBuilder":
        self._bike.range_km = km
        return self

    def set_charge_time(self, time_str: str) -> "ConcreteElectricBikeBuilder":
        self._bike.charge_time = time_str
        return self

    def build(self) -> ElectricBike:
        result = self._bike
        self._bike = ElectricBike()
        return result


class Director:
    def __init__(self, builder: BikeBuilder):
        self._builder = builder

    @property
    def builder(self) -> BikeBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: BikeBuilder):
        self._builder = builder

    def create_order(
        self,
        frame: str,
        wheels: str,
        brakes: str,
        gears: str,
        color: str,
        price: float,
        **extra_kwargs,
    ) -> Product:
        self._builder.set_frame(frame)
        self._builder.set_wheels(wheels)
        self._builder.set_brakes(brakes)
        self._builder.set_gears(gears)
        self._builder.set_color(color)
        self._builder.set_price(price)

        if isinstance(self._builder, ConcreteElectricBikeBuilder):
            self._builder.set_battery(extra_kwargs.get("battery", ""))
            self._builder.set_motor(extra_kwargs.get("motor", ""))
            self._builder.set_range(extra_kwargs.get("range_km", 0))
            self._builder.set_charge_time(extra_kwargs.get("charge_time", ""))

        return self._builder.build()
