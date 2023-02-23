import datetime

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from expense.models import Expense
from income.models import Income


class ExpenseSummaryStats(APIView):

    def get_amount_for_expense(self, expense_list, category):
        expenses = expense_list.filter(expense_category=category)
        amount = 0

        for expense in expenses:
            amount += expense.amount

        return {'amount': str(amount)}

    def get_category(self, expense):
        return expense.expense_category

    def get(self, request):
        todays_date = datetime.date.today()
        a_year_ago_date = todays_date - datetime.timedelta(days=365)
        expenses = Expense.objects.filter(
            owner=request.user, created_at__gte=a_year_ago_date, created_at__lte=todays_date)

        final = {}

        categories = list(set(map(self.get_category, expenses)))

        for expense in expenses:
            for category in categories:
                final[category] = self.get_amount_for_expense(
                    expense, category)

        return Response(data={
            'category_data': final
        }, status=status.HTTP_200_OK)


class IncomeSummaryStats(APIView):

    def get_amount_for_income(self, income_list, category):
        incomes = income_list.filter(income_category=category)
        amount = 0

        for income in incomes:
            amount += income.amount

        return {'amount': str(amount)}

    def get_category(self, income):
        return income.income_category

    def get(self, request):
        todays_date = datetime.date.today()
        a_year_ago_date = todays_date - datetime.timedelta(days=365)
        incomes = Income.objects.filter(
            owner=request.user, created_at__gte=a_year_ago_date, created_at__lte=todays_date)

        final = {}

        categories = list(set(map(self.get_category, incomes)))

        for income in incomes:
            for category in categories:
                final[category] = self.get_amount_for_income(
                    income, category)

        return Response(data={
            'category_data': final
        }, status=status.HTTP_200_OK)
