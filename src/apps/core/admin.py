from django.contrib import admin
from .models import (
    Level, SavingsGoal, BankAccount, Transaction, SavingsContribution, 
    SavingsLevel, SavingsGame, SavingsGroup, Participant, PaymentTurn
)

admin.site.register(Level)
admin.site.register(SavingsGoal)
admin.site.register(BankAccount)
admin.site.register(Transaction)
admin.site.register(SavingsContribution)
admin.site.register(SavingsLevel)
admin.site.register(SavingsGame)
admin.site.register(SavingsGroup)
admin.site.register(Participant)
admin.site.register(PaymentTurn)

