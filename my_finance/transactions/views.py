from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.timezone import now, timedelta
from django.contrib import messages

from .models import Income, Expense


class BadRequestException(Exception):

    def __init__(self, msg):
        self.msg = msg


# Create your views here.
@login_required(login_url='auth:login')
def index(request):
    return redirect("transactions:index")


@login_required(login_url='auth:login')
def transactions(request):
    return render(request, "transactions/transactions.html")


@login_required(login_url='auth:login')
def statistics(request):
    user = request.user
    incomes = Income.objects.filter(user=user).order_by('-created_at')
    expenses = Expense.objects.filter(user=user).order_by('-created_at')
    total_income = sum([income.amount for income in incomes])
    total_expenses = sum([expense.amount for expense in expenses])
    balance = total_income - total_expenses
    context = {
        "incomes": incomes,
        "expenses": expenses,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
    }
    return render(request, "transactions/statistics.html", context)


@login_required(login_url='auth:login')
def create_income_transaction(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        created_at = request.POST['created']
        description = request.POST['description']
        category = request.POST['category']
        print(amount, created_at, description, category)
        if not amount:
            messages.add_message(request, messages.ERROR, 'Amount is required')
            return render(request, "transactions/transactions.html", {'amount': amount})
        if created_at == '':
            created_at = now()
        new_income = Income(amount=amount, created_at=created_at, description=description, category=category)
        new_income.user_id = request.user.id
        new_income.save()
        return redirect(reverse('transactions:statistics'))
    return render(request, "transactions/transaction.html")


@login_required(login_url='auth:login')
def create_expense_transaction(request):
    if request.method == 'POST':
        amount_exp = request.POST.get('amount_exp')
        date = request.POST.get('created_exp')
        desc = request.POST.get('description_exp')
        category = request.POST.get('category_exp')
        print(amount_exp, date, desc, category)
        if not amount_exp:
            messages.add_message(request, messages.ERROR, 'Amount is required')
            return render(request, "transactions/transactions.html", {'amount_exp': amount_exp})
        if date == '':
            date = now()
        new_expense = Expense(amount=amount_exp, created_at=date, description=desc, category=category)
        new_expense.user_id = request.user.id
        new_expense.save()
        return redirect(reverse('transactions:statistics'))
    return render(request, "transactions/transaction.html")


@login_required(login_url='auth:login')
def delete_income_transaction(request, income_id):
    income = get_object_or_404(Income, pk=income_id, user=request.user)
    income.delete()
    return redirect(reverse('transactions:statistics'))


@login_required(login_url='auth:login')
def delete_expense_transaction(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id, user=request.user)
    expense.delete()
    return redirect(reverse('transactions:statistics'))


@login_required(login_url='auth:login')
def filter_income_transaction(request):
    if request.method == 'POST':
        inc_date_from = request.POST.get('inc_date_from')
        inc_date_to = request.POST.get('inc_date_to')
        print(inc_date_from, inc_date_to)
        if inc_date_from == '':
            inc_date_from = now()-timedelta(days=365)
        if inc_date_to == '':
            inc_date_to = now()

        incomes = Income.objects.filter(created_at__range=[inc_date_from, inc_date_to])
        return render(request, "transactions/statistics.html", {'incomes': incomes})
    return render(request, "transactions/statistics.html")


@login_required(login_url='auth:login')
def filter_expense_transaction(request):
    if request.method == 'POST':
        exp_date_from = request.POST.get('exp_date_from')
        exp_date_to = request.POST.get('exp_date_to')
        print(exp_date_from, exp_date_to)
        if exp_date_from == '':
            exp_date_from = now()-timedelta(days=365)
        if exp_date_to == '':
            exp_date_to = now()

        expenses = Expense.objects.filter(created_at__range=[exp_date_from, exp_date_to])
        return render(request, "transactions/statistics.html", {'expenses': expenses})
    return render(request, "transactions/statistics.html")
