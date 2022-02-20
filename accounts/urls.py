from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.CustomLoginView.as_view(), name="login"),
    path("", LogoutView.as_view(next_page="main_home"), name="logout"),
]
