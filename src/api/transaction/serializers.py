from rest_framework import serializers
from apps.core.models import Transaction

class TransactionSummarySerializer(serializers.Serializer):
    date = serializers.DateField()
    income = serializers.DecimalField(max_digits=10, decimal_places=2)
    expense = serializers.DecimalField(max_digits=10, decimal_places=2)
    profit = serializers.DecimalField(max_digits=10, decimal_places=2)
    savings = serializers.DecimalField(max_digits=10, decimal_places=4)  # Ajustado a 4 decimales según tu ejemplo


