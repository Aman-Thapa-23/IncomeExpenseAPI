from django.urls import path, include
from .views import *

app_name = 'userstats'

urlpatterns = [
    path('user-expense-stats/', ExpenseSummaryStats.as_view(), name='user-expense-stats'),
    path('user-income-stats/', IncomeSummaryStats.as_view(), name='user-income-stats'),
]