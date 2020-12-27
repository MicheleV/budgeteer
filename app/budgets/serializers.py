# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from rest_framework import serializers

from budgets.models import Category
from budgets.models import Expense
from budgets.models import MonthlyBalance


class CategorySerializer(serializers.HyperlinkedModelSerializer):  # pylint: disable=C0115; # noqa
    class Meta:  # pylint: disable=C0115,R0903; # noqa
        model = Category
        fields = ['id', 'text']


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):  # pylint: disable=C0115; # noqa
    category_text = serializers.CharField(source='category.text')

    class Meta:  # pylint: disable=C0115,R0903; # noqa
        model = Expense
        fields = ['id', 'amount', 'category_id', 'category_text', 'note', 'date']


class MonthlyBalanceSerializer(serializers.HyperlinkedModelSerializer):  # pylint: disable=C0115; # noqa
    category_text = serializers.CharField(source='category.text')

    class Meta:  # pylint: disable=C0115,R0903; # noqa
        model = MonthlyBalance
        fields = ['id', 'amount', 'category_id', 'category_text', 'date']
