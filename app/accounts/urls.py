from django.contrib.auth import views as auth_views
from django.urls import path

from accounts import views

app_name = 'accounts'  # pylint: disable=C0103; # noqa
urlpatterns = [
  path('index/', views.index, name='index'),

  path('signup/', views.SignUpView.as_view(), name='signup'),
  path('login/', auth_views.LoginView.as_view(), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
