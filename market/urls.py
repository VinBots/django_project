from django.urls import path
from . import views

urlpatterns = [
    path('', views.market_home, name='market_home'),
    ]