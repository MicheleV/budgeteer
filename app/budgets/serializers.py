# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os

from rest_framework import serializers

from budgets.models import Category
from budgets.models import Expense
from budgets.models import MonthlyBalanceCategory
from budgets.models import MonthlyBalance


class CategorySerializer(serializers.ModelSerializer):  # pylint: disable=C0115; # noqa
    class Meta:  # pylint: disable=C0115,R0903; # noqa
        model = Category
        fields = ['id', 'text']


class ExpenseSerializer(serializers.ModelSerializer):  # pylint: disable=C0115; # noqa
    category_text = serializers.CharField(source='category.text')

    class Meta:  # pylint: disable=C0115,R0903; # noqa
        model = Expense
        fields = ['id', 'amount', 'category_id', 'category_text', 'note', 'date']


class MonthlyBalanceCategorySerializer(serializers.ModelSerializer):  # pylint: disable=C0115; # noqa
    class Meta:  # pylint: disable=C0115,R0903; # noqa
        model = MonthlyBalanceCategory
        fields = ['id', 'text', 'is_foreign_currency']


class MonthlyBalanceSerializer(serializers.ModelSerializer):  # pylint: disable=C0115; # noqa
    category_text = serializers.CharField(source='category.text')
    category_is_foreign_currency = serializers.BooleanField(source='category.is_foreign_currency')
    amount = serializers.SerializerMethodField()

    def get_amount(self, obj):  # pylint: disable=R0201; # noqa
        rate = int(os.getenv("EXCHANGE_RATE"))
        if obj.category.is_foreign_currency:
            return obj.amount * rate
        return obj.amount

    class Meta:  # pylint: disable=C0115,R0903; # noqa
        model = MonthlyBalance
        fields = ['id', 'amount', 'category_id', 'category_text', 'category_is_foreign_currency', 'date']
