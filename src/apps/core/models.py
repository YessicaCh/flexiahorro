from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


# class RoleChoices(models.TextChoices):
#     ADMIN = 'admin', _('Admin')
#     COLLABORATOR = 'collaborator', _('Collaborator')
#     USER = 'user', _('User')

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     email = models.EmailField(max_length=100, unique=True)
#     email_token = models.CharField(max_length=100, blank=True, null=True)
#     forget_password_token = models.CharField(max_length=100, blank=True, null=True)
#     is_verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     role = models.CharField(max_length=20, choices=RoleChoices.choices, default=RoleChoices.COLLABORATOR)

#     def __str__(self):
#         return self.user.username

#     def save(self, *args, **kwargs):
#         """Asegura que el email del perfil coincida con el del usuario."""
#         self.user.email = self.email
#         self.user.save()
#         super().save(*args, **kwargs)

#     class Meta:
#         verbose_name = _("User Profile")
#         verbose_name_plural = _("User Profiles")

class Level(models.Model):
    name = models.CharField(max_length=255)  # Nombre del nivel
    difficulty = models.IntegerField()  # Dificultad del nivel (1-10)
    num_goals = models.IntegerField(default=1)  # Número de metas en el nivel
    description = models.TextField(blank=True, null=True)  # Descripción opcional

    def __str__(self):
        return self.name  # Representación en el admin


class SavingsModeChoices(models.TextChoices):
    PERCENTAGE = "percentage", "Porcentaje"
    FIXED_AMOUNT = "fixed", "Monto Fijo"
    ROUNDING = "rounding", "Vuelto"
    RANGE = "range", "Rango"

class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="savings_goals")
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    savings_mode = models.CharField(
        max_length=20,
        choices=SavingsModeChoices.choices,
        default=SavingsModeChoices.PERCENTAGE
    )

    # Opciones según el modo de ahorro
    percentage_value = models.IntegerField(
        choices=[(5, "5%"), (10, "10%"), (15, "15%")],
        null=True, blank=True,
        help_text="Debe elegir entre 5, 10 o 15% si selecciona 'Porcentaje'"
    )
    fixed_amount = models.DecimalField(
        max_digits=10, decimal_places=2, 
        null=True, blank=True,
        help_text="Debe ingresar un monto fijo si selecciona 'Monto Fijo'"
    )
    rounding_to = models.IntegerField(
        choices=[(5, "Próximo 5"), (10, "Próximo 10")],
        null=True, blank=True,
        help_text="Debe elegir si se redondea al próximo 5 o 10 si selecciona 'Vuelto'"
    )
    range_start = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text="Debe ingresar el inicio del rango si selecciona 'Rango'"
    )
    range_end = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text="Debe ingresar el fin del rango si selecciona 'Rango'"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def clean(self):
        """Validaciones según el modo de ahorro seleccionado"""
        if self.savings_mode == SavingsModeChoices.PERCENTAGE and not self.percentage_value:
            raise ValidationError("Debe seleccionar un valor de porcentaje (5%, 10% o 15%).")
        if self.savings_mode == SavingsModeChoices.FIXED_AMOUNT and not self.fixed_amount:
            raise ValidationError("Debe ingresar un monto fijo.")
        if self.savings_mode == SavingsModeChoices.ROUNDING and not self.rounding_to:
            raise ValidationError("Debe seleccionar si redondea al próximo 5 o 10.")
        if self.savings_mode == SavingsModeChoices.RANGE:
            if not self.range_start or not self.range_end:
                raise ValidationError("Debe ingresar valores de inicio y fin para el rango.")
            if self.range_start >= self.range_end:
                raise ValidationError("El valor de inicio debe ser menor al de fin.")

    def __str__(self):
        return f"{self.name} - {self.savings_mode} - S/. {self.amount}"

class DailySaving(models.Model):
    date = models.DateField(unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    savings_goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE, related_name="daily_savings", null=True, blank=True)

    def __str__(self):
        return f"Ahorro {self.amount} en {self.date} para {self.savings_goal.name if self.savings_goal else 'Sin meta'}"


class AccountTypeChoices(models.TextChoices):
    SAVINGS = "savings", _("Ahorro")
    CHECKING = "checking", _("Corriente")

class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bank_accounts")
    account_number = models.CharField(max_length=20, unique=True)
    bank_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=50, choices=AccountTypeChoices.choices)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"

class TransactionTypeChoices(models.TextChoices):
    INCOME = "income", _("Ingreso")
    EXPENSE = "expense", _("Egreso")

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_type = models.CharField(max_length=50, choices=TransactionTypeChoices.choices)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - S/. {self.amount}"















class SavingsContribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="savings_contributions")
    percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Porcentaje de ahorro")
    linked_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="contributions")

    def __str__(self):
        return f"{self.percentage}% de ahorro"

class SavingsLevel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="savings_levels")
    level = models.PositiveIntegerField()
    unlocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nivel {self.level} - {self.user.username}"

class SavingsGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="savings_games")
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PaymentPeriodChoices(models.TextChoices):
    WEEKLY = "weekly", _("Semanal")
    MONTHLY = "monthly", _("Mensual")

class SavingsGroup(models.Model):
    game = models.ForeignKey(SavingsGame, on_delete=models.CASCADE, related_name="groups")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_period = models.CharField(max_length=50, choices=PaymentPeriodChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Junta - {self.amount} - {self.payment_period}"

class Participant(models.Model):
    group = models.ForeignKey(SavingsGroup, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="savings_groups")
    order = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} en {self.group}"

class PaymentTurn(models.Model):
    group = models.ForeignKey(SavingsGroup, on_delete=models.CASCADE, related_name="turns")
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="turns")
    due_date = models.DateField()

    def __str__(self):
        return f"Turno de {self.participant.user.username} - {self.due_date}"