# Copyright: (c) 2020, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# $ python manage.py shell
# (InteractiveConsole)
# import budgets.models as m
# from django.db.models import Avg, Count, Min, Sum

# cats = m.Category.objects.all()
# for cat in cats:
#     expenses = m.Expense.objects.filter(category_id=cat.id)
#     for e in expenses:
#         print(e)
#     expenses_sum = sum(ex.amount for ex in expenses)
#     cat.total = expenses_sum
#     print(f"Category id: {cat.id} ({cat.text}) total is {expenses_sum}... that should be equal to {cat.total}")
