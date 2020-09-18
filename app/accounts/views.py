from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView

@login_required
def index(request):
    return render(request, 'accounts/index.html')


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('budgets:expenses')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid
