from django.core.management.base import BaseCommand
from store.models import BikeModel


class Command(BaseCommand):
    help = "Заповнює каталог зразковими велосипедами (regular + electric)"

    def handle(self, *args, **options):
        if BikeModel.objects.exists():
            self.stdout.write(self.style.WARNING(
                "Каталог уже містить дані. Пропускаємо. "
                "Для повторного заповнення — очистіть таблицю BikeModel."
            ))
            return

        regular_bikes = [
            {
                "name": "CityRider Pro",
                "bike_type": "regular",
                "frame": "Алюмінієва 6061, 52 см",
                "wheels": "700c, подвійний обід",
                "brakes": "Дискові гідравлічні Shimano",
                "gears": "Shimano Deore, 21 швидкість",
                "color": "Матовий чорний",
                "price": 18500,
                "description": (
                    "Ідеальний міський велосипед для щоденних поїздок. "
                    "Легка алюмінієва рама, надійні гідравлічні гальма "
                    "та 21 швидкість для будь-якого рельєфу."
                ),
            },
            {
                "name": "MountainKing XT",
                "bike_type": "regular",
                "frame": "Карбонова, 48 см",
                "wheels": "29\", Maxxis Ardent",
                "brakes": "Shimano XT, 4 поршні",
                "gears": "SRAM Eagle, 12 швидкостей",
                "color": "Синій металік",
                "price": 32000,
                "description": (
                    "Професійний гірський велосипед з карбоновою рамою. "
                    "Створений для серйозних трейлів та складних "
                    "маршрутів у горах."
                ),
            },
            {
                "name": "SpeedWing Aero",
                "bike_type": "regular",
                "frame": "Карбонова аеро, 54 см",
                "wheels": "700c, аеродинамічний профіль",
                "brakes": "Дискові Ultegra",
                "gears": "Shimano Ultegra, 22 швидкості",
                "color": "Червоний / Чорний",
                "price": 45000,
                "description": (
                    "Шосейний велосипед для швидкісних поїздок "
                    "та змагань. Аеродинамічна карбонова рама "
                    "мінімізує опір повітря."
                ),
            },
            {
                "name": "ComfortCruise Classic",
                "bike_type": "regular",
                "frame": "Сталева ретро, 50 см",
                "wheels": "26\", широкий протектор",
                "brakes": "Ободові V-brake",
                "gears": "Shimano Tourney, 7 швидкостей",
                "color": "Бежевий / Коричневий",
                "price": 12500,
                "description": (
                    "Класичний круїзер для неспішних прогулянок "
                    "містом. Комфортна посадка, широке сідло "
                    "та стильний ретро-дизайн."
                ),
            },
            {
                "name": "TrailBlazer Junior",
                "bike_type": "regular",
                "frame": "Алюмінієва, 44 см",
                "wheels": "26\", Kenda",
                "brakes": "Дискові механічні",
                "gears": "Shimano Altus, 18 швидкостей",
                "color": "Зелений / Жовтий",
                "price": 9800,
                "description": (
                    "Надійний велосипед для початківців та підлітків. "
                    "Легка рама, простий у обслуговуванні "
                    "та дуже витривалий."
                ),
            },
        ]

        electric_bikes = [
            {
                "name": "VoltStorm E750",
                "bike_type": "electric",
                "frame": "Алюмінієва гідроформована, 50 см",
                "wheels": "27.5\", широкі Schwalbe",
                "brakes": "Гідравлічні Tektro 4P",
                "gears": "Shimano Deore, 10 швидкостей",
                "color": "Темно-сірий / Зелений",
                "price": 55000,
                "battery_capacity": "48V 14Ah, Samsung Li-Ion",
                "motor_power": "Bafang 750W",
                "range_km": 80,
                "charge_time": "4-5 годин",
                "description": (
                    "Потужний електровелосипед для будь-яких умов. "
                    "Мотор 750W забезпечує легкий підйом на круті "
                    "схили, а ємний акумулятор Samsung — "
                    "до 80 км на одному заряді."
                ),
            },
            {
                "name": "EcoGlide City",
                "bike_type": "electric",
                "frame": "Алюмінієва Step-Through, 48 см",
                "wheels": "28\", антипрокольні",
                "brakes": "Гідравлічні Shimano",
                "gears": "Планетарна Nexus, 7 швидкостей",
                "color": "Білий перламутр",
                "price": 42000,
                "battery_capacity": "36V 10Ah, LG",
                "motor_power": "Bafang 250W (задній)",
                "range_km": 60,
                "charge_time": "3-4 години",
                "description": (
                    "Елегантний міський електровелосипед з низькою "
                    "рамою. Ідеальний для щоденних поїздок "
                    "на роботу та по магазинах."
                ),
            },
            {
                "name": "ThunderBolt MTB-E",
                "bike_type": "electric",
                "frame": "Карбонова full-suspension, 52 см",
                "wheels": "29\", Maxxis Minion",
                "brakes": "Shimano Saint, 4 поршні",
                "gears": "SRAM GX Eagle, 12 швидкостей",
                "color": "Чорний / Помаранчевий",
                "price": 89000,
                "battery_capacity": "48V 17.5Ah, Panasonic",
                "motor_power": "Shimano EP8, 250W номінал",
                "range_km": 120,
                "charge_time": "5-6 годин",
                "description": (
                    "Преміальний електричний гірський велосипед "
                    "з мотором Shimano EP8. Повна підвіска для "
                    "максимального комфорту на будь-яких трейлах."
                ),
            },
            {
                "name": "SwiftFold E-Compact",
                "bike_type": "electric",
                "frame": "Алюмінієва складна, регульована",
                "wheels": "20\", компактні",
                "brakes": "Дискові механічні",
                "gears": "Shimano Tourney, 7 швидкостей",
                "color": "Сріблястий",
                "price": 28000,
                "battery_capacity": "36V 7.8Ah, знімний",
                "motor_power": "Rear Hub 250W",
                "range_km": 35,
                "charge_time": "2-3 години",
                "description": (
                    "Компактний складний електровелосипед. "
                    "Ідеальний для мультимодальних поїздок — "
                    "легко поміщається в багажник авто "
                    "або громадський транспорт."
                ),
            },
        ]

        created = 0
        for bike_data in regular_bikes + electric_bikes:
            BikeModel.objects.create(**bike_data)
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Створено {created} велосипедiв у каталозi "
            f"({len(regular_bikes)} звичайних + {len(electric_bikes)} електро)"
        ))
