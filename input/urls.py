from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="input"),
    path("ghg/view/", views.GHGList.as_view(), name="ghg"),
    path("ghg/update/<int:pk>/", views.GHGListUpdate.as_view(), name="update-ghg"),
    path("ghg/create/", views.GHGListCreate.as_view(), name="create-ghg")
    # path("targets/view/", GHGList.as_view(), name="ghg"),
    # path("targets/update/<int:pk>/", GHGListUpdate.as_view(), name="update-targets"),
    # path("targets/create/", GHGListCreate.as_view(), name="create-targets"),
]
