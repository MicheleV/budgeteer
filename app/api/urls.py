# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import path

from api import views

app_name = 'api'  # pylint: disable=C0103; # noqa
urlpatterns = [
    path('categories', views.all_categories, name='categories'),
    path('expenses', views.all_expenses, name='expenses'),
]
