# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import path
from django.urls import re_path
import debug_toolbar
from api import views

app_name = 'api'
urlpatterns = [
    path('categories', views.api_categories, name='categories'),
]
