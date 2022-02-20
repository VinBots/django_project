from django.urls import path
from . import views
from .views import GHGList, GHGListCreate, GHGListUpdate

urlpatterns = [
    path("ghg/view/", GHGList.as_view(), name="ghg"),
    path("ghg/update/<int:pk>/", GHGListUpdate.as_view(), name="update-ghg"),
    path("ghg/create/", GHGListCreate.as_view(), name="create-ghg")
    # path("targets/view/", GHGList.as_view(), name="ghg"),
    # path("targets/update/<int:pk>/", GHGListUpdate.as_view(), name="update-targets"),
    # path("targets/create/", GHGListCreate.as_view(), name="create-targets"),
]
