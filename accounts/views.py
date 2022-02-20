from re import template
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy


class CustomLoginView(LoginView):

    template_name = "django_project/accounts/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("input")

class CustomLogoutView(LogoutView):
