from django.urls import path
from . import views

urlpatterns = [
    path("", views.CustomLoginView.as_view(), name="login"),
]
