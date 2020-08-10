"""budgeteer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.urls import path, include
from django.conf.urls import url

# Note: Regex /?P<date>(19|20)[0-9]{2}-(0[1-9]|1[012]))/
# allow only dates between 1900-01 and 2099-12
# Warning: month is always two digits (i.e. Jan -> '01', not '1')
urlpatterns = [
    path('', include('budgets.urls')),
]

if 'y' in os.getenv("DJANGO_DEBUG_MODE"):
    import debug_toolbar
    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
