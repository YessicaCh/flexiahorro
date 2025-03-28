from rest_framework import routers
from django.urls import path, include
from .views import DailyProfitView, TransactionReportView



urlpatterns = [
    path("transactions/daily-profit/", DailyProfitView.as_view(), name="daily-profit"),
    path("transactions/report/", TransactionReportView.as_view(), name="transaction-report"),
]

