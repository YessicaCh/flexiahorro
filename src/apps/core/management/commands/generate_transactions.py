import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from apps.core.models import Transaction, User  # Asegúrate de que "myapp" sea tu aplicación

class Command(BaseCommand):
    help = "Genera transacciones aleatorias para hoy y ayer"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, default=500, help="Número de transacciones a generar"
        )

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        users = list(User.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR("No hay usuarios en la base de datos."))
            return

        transaction_types = ["income", "expense"]
        transactions = []

        for _ in range(count):
            user = random.choice(users)
            amount = round(random.uniform(1, 50), 2)
            transaction_type = random.choice(transaction_types)

            # Fecha aleatoria entre hoy y ayer
            random_days = random.choice([0, 1])
            random_time = timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
            transaction_date = make_aware(datetime.now() - timedelta(days=random_days) + random_time)

            transactions.append(
                Transaction(
                    user=user,
                    amount=amount,
                    transaction_type=transaction_type,
                    date=transaction_date
                )
            )

        Transaction.objects.bulk_create(transactions)

        self.stdout.write(self.style.SUCCESS(f"✅ {count} transacciones generadas con éxito."))
