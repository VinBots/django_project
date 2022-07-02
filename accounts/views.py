from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CreateUserForm


class CustomLoginView(LoginView):

    template_name = "django_project/accounts/login.html"
    fields = "__all__"
    redirect_authenticated_user = True


def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account as created for " + user)
            return redirect("login")
    context = {"form": form}
    return render(request, "django_project/accounts/register.html", context)


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = "django_project/accounts/register.html"
    success_url = reverse_lazy("login")
    form_class = CreateUserForm
    success_message = "Your account was created successfully"
