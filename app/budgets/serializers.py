# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from rest_framework import serializers

from budgets.models import Category, Expense


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'text']


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    category_text = serializers.CharField(source='category.text')

    class Meta:
        model = Expense
        fields = ['id', 'amount', 'category_id', 'category_text', 'note', 'date']
