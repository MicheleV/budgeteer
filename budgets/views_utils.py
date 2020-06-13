# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import calendar
import datetime
from dateutil.relativedelta import relativedelta
import math
import os

from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.db.models import F
from django.db.models import Case
from django.db.models import When
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from graphs import plot

import budgets.forms as f
import budgets.models as m


def get_previous_month_first_day_date(date):
    """
    Return the first day of the previous month
    """
    return (date - relativedelta(months=1)).replace(day=1)


def get_total_of_monthly_balances(date):
    """
    Return the sum of the monthly balances for the input date
    """
    rate = int(os.getenv("EXCHANGE_RATE"))
    balances = m.MonthlyBalance.objects.select_related('category').filter(date=date)
    return balances.aggregate(correct_sum=Sum(Case(
      When(category__is_foreign_currency=False, then='amount'),
      When(category__is_foreign_currency=True, then=F('amount') * rate)
    )))['correct_sum']


def get_month_boundaries(date=None):
    """
    Return a tuple composed of the first and the last day
    of month passed as parameter, as datetime objects

    Note: set timezone when providing! Otherwise efault timezone will be UTC
    If th server is actually in a different time zone, beware off-by-one
    month errors when using this function
    """
    if not date:
        start = datetime.date.today().replace(day=1)
    else:
        complete_date = f"{date}-01"
        format_str = '%Y-%m-%d'
        start = datetime.datetime.strptime(complete_date, format_str).date()

    month_range = calendar.monthrange(start.year, start.month)
    last_day_of_month = month_range[1]
    end = datetime.date(start.year, start.month, last_day_of_month)
    return (start, end)


def current_month_boundaries():
    """
    Return a tuple composed of the first and the last day
    of the current month, as datetime objects

    Note: set timezone when providing! Otherwise efault timezone will be UTC
    If th server is actually in a different time zone, beware off-by-one
    month errors when using this function
    """
    start = datetime.date.today().replace(day=1)
    month_range = calendar.monthrange(start.year, start.month)
    last_day_of_month = month_range[1]
    end = datetime.date(start.year, start.month, last_day_of_month)
    return (start, end)


def generate_monthly_balance_bar_graph(data, goals):
    """
    Return a base64 string making up the graph or false
    """
    if len(data) > 1:
        dates = []
        amounts = []
        for val in data:
            dates.append(val['date'])
            try:
                amounts.append(val['actual_amount'])
            except (AttributeError, NameError, KeyError) as e:
                print("You've forgot to add actual_amount somewhere (bar)")
                amounts.append(val['amount'])
        return plot.generateBarGraph(dates, amounts, goals)

    return False


def generate_current_monthly_balance_pie_graph(data):
    """
    Return a base64 string making up the graph or false
    """
    if len(data) > 1:
        labels = []
        values = []
        for mb in filter(lambda y: y.amount > 0, data):
            labels.append(mb.category.text)
            # TODO: remove this once all places calling this function are
            # passing monthly budgets with actual_ammount attribute
            try:
                values.append(mb.actual_amount)
            except AttributeError as e:
                print("You've forgot to add actual_amount somewhere (pie)")
                values.append(mb.amount)
        return plot.generatePieGraph(labels, values)
    return False


# Credits https://stackoverflow.com/a/58612038
def findInList(List, item):
    """
    Return the index of item inside List, or -1 if not found
    """
    try:
        return List.index(item)
    except ValueError:
        return -1


def aggregate_expenses_by_category(data):
    results = {}
    for mb in filter(lambda y: y.amount > 0, data):
        if mb.category.id in results:
            results[mb.category.id] += mb.amount
        else:
            results[mb.category.id] = mb.amount
    return results


def generate_current_month_expenses_pie_graph(data):
    """
    Return the graph and returns the data in base64
    Return boolean representing whether a graph was generated or not
    """
    if len(data) > 1:
        labels = []
        values = []

        # NOTE: this ugly block saves us one query... is it worth it?
        for mb in filter(lambda y: y.amount > 0, data):
            index = findInList(labels, mb.category.text)
            if index == -1:
                labels.append(mb.category.text)
                values.append(mb.amount)
            else:
                values[index] = values[index] + mb.amount

        return plot.generatePieGraph(labels, values)
    return False


def append_year_and_month_to_url(obj, named_url, delete=False):
    """
    Return an url with obj's date appended in YYYY-mm format
    """
    format_str = '%Y-%m'
    date_ym = obj.date.strftime(format_str)
    view_url = reverse(named_url)
    redirect_url = f"{view_url}/{date_ym}"
    if delete:
        redirect_url = f"{redirect_url}?delete=1"
    return redirect_url


def get_goals_and_time_to_completions(current_mb_total, two_months_diff):
    """
    Returns non archived goals with how many months will it take to complete
    """
    # Display bar graph (only draw "active" goals)
    goals = m.Goal.objects.filter(is_archived=False)
    # Calculate time to complete each goal given the last two months difference
    for goal in goals:
        if current_mb_total >= goal.amount:
            goal.months_to_go = 0
        elif two_months_diff < 0:
            # Handle case where the balance has decreased
            goal.months_to_go = None
        else:
            diff = goal.amount - current_mb_total
            try:
                months_to_go = diff / two_months_diff
            except ZeroDivisionError:
                months_to_go = 0
            goal.months_to_go = math.ceil(months_to_go)
    return goals


def get_month_balance_stats(date, rate):
    """
    Return monthly balances and their sum (adjusted to local currency)
    """
    import pdb
    prev_mb = m.MonthlyBalance.objects.select_related('category').filter(
              date=date).order_by('category_id')
    total = 0
    for mv in prev_mb:
        if mv.category.is_foreign_currency:
            total += mv.amount * rate
        else:
            total += mv.amount
    return prev_mb, total


def calc_increase_perc(current_mb_total, prev_mb_total):
    """
    TODO write me
    """
    if current_mb_total is None:
        current_mb_total = 0
        two_months_diff = 0
        two_months_diff_perc = 0
    elif prev_mb_total is None or prev_mb_total == 0:
        two_months_diff = current_mb_total
        two_months_diff_perc = None
    else:
        two_months_diff = current_mb_total - prev_mb_total
        two_months_diff_perc = (current_mb_total / prev_mb_total * 100) - 100
        # Truncate to two decimals
        two_months_diff_perc = '%.2f' % (two_months_diff_perc)
    return current_mb_total, two_months_diff, two_months_diff_perc
