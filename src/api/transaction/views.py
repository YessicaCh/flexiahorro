from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.core.models import Transaction, SavingsGoal, SavingsModeChoices, DailySaving
from .serializers import TransactionSummarySerializer
from django.db.models.functions import TruncDay, TruncMonth, Coalesce
from django.db.models import Sum, Value, DecimalField, Q
from django.db.models.functions import Coalesce
from pprint import pprint



class DailyProfitView(APIView):
    def get(self, request):
        date_str = request.query_params.get("date", None)
        if date_str:
            try:
                query_date = make_aware(datetime.strptime(date_str, "%Y-%m-%d"))
            except ValueError:
                return Response({"error": "Formato de fecha inválido (YYYY-MM-DD)"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            query_date = make_aware(datetime.now())

        transactions = Transaction.objects.filter(date__date=query_date.date())

        summary = transactions.aggregate(
            income=Sum("amount", filter=Q(transaction_type="income")) or 0,
            expense=Sum("amount", filter=Q(transaction_type="expense")) or 0
        )
        summary["profit"] = summary["income"] - summary["expense"]

        if summary["profit"] <= 0:
            summary["savings"] = 0
        else:
            user = request.user
            savings_goals = SavingsGoal.objects.filter(user=user, is_active=True)

            total_savings = 0
            for goal in savings_goals:
                if goal.savings_mode == SavingsModeChoices.PERCENTAGE:
                    total_savings += (summary["profit"] * goal.percentage_value / 100)

                elif goal.savings_mode == SavingsModeChoices.FIXED_AMOUNT:
                    total_savings += goal.fixed_amount

                elif goal.savings_mode == SavingsModeChoices.ROUNDING:
                    if goal.rounding_to == 5:
                        total_savings += (5 - (summary["profit"] % 5)) if summary["profit"] % 5 != 0 else 0
                    elif goal.rounding_to == 10:
                        total_savings += (10 - (summary["profit"] % 10)) if summary["profit"] % 10 != 0 else 0

                elif goal.savings_mode == SavingsModeChoices.RANGE:
                    if goal.range_start <= summary["profit"] <= goal.range_end:
                        total_savings += summary["profit"]

            summary["savings"] = max(0, total_savings)

            if summary["savings"] > 0:
                daily_saving, created = DailySaving.objects.get_or_create(
                    date=query_date.date(), defaults={"amount": summary["savings"]}
                )
                if not created:
                    daily_saving.amount = summary["savings"]
                    daily_saving.save()

        # 🔹 Convertir el diccionario en un objeto con atributos para evitar KeyError
        class SummaryObject:
            def __init__(self, data):
                for key, value in data.items():
                    setattr(self, key, value)

        summary["date"] = query_date.date().strftime("%Y-%m-%d")  # Agregar la fecha como string
        summary_obj = SummaryObject(summary)  # Convertir el diccionario en un objeto

        pprint(summary)

        return Response(TransactionSummarySerializer(summary_obj).data, status=status.HTTP_200_OK)





class TransactionReportView(APIView):
    """
    Endpoint para obtener reportes agrupados por día o mes.
    Parámetro `filter_type`: "daily" o "monthly".
    """

    @extend_schema(
        summary="Obtener reportes de ingresos, egresos y ganancias",
        description="Retorna la suma de ingresos, egresos y ganancia neta agrupados por día o mes.",
        parameters=[
            OpenApiParameter(
                name="filter_type",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Filtro para agrupar la data: 'daily' para diario, 'monthly' para mensual.",
                required=False,
                enum=["daily", "monthly"]
            )
        ],
        responses={
            200: "Lista de transacciones agrupadas con income, expense y profit.",
            400: "Error de validación en los parámetros de consulta."
        }
    )
    def get(self, request):
        filter_type = request.query_params.get("filter_type", "daily")  # "daily" por defecto
        
        if filter_type not in ["daily", "monthly"]:
            return Response({"error": "Filtro inválido. Use 'daily' o 'monthly'."}, status=status.HTTP_400_BAD_REQUEST)

        date_trunc = TruncDay("date") if filter_type == "daily" else TruncMonth("date")

        transactions = (
            Transaction.objects
            .annotate(period=date_trunc)  # Agrupar por día o mes
            .values("period")
            .annotate(
                income=Coalesce(Sum("amount", filter=Q(transaction_type="income"), output_field=DecimalField()), Value(0, output_field=DecimalField())),
                expense=Coalesce(Sum("amount", filter=Q(transaction_type="expense"), output_field=DecimalField()), Value(0, output_field=DecimalField()))
            )
            .order_by("period")
        )

        # Construir la respuesta formateada
        response_data = [
            {
                "date": transaction["period"].strftime("%Y-%m") if filter_type == "monthly" else transaction["period"].strftime("%Y-%m-%d"),
                "income": float(transaction["income"]),
                "expense": float(transaction["expense"]),
                "profit": float(transaction["income"] - transaction["expense"])
            }
            for transaction in transactions
        ]

        return Response(response_data, status=status.HTTP_200_OK)
