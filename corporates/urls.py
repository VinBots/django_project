from django.urls import path
from . import views
from .views import GHGList, GHGListUpdate

urlpatterns = [
    path("<str:corp_name>/", views.corporates_search, name="corporates_search"),
    path("", views.corporates_home, name="corporates_home"),
    path(
        "charts/html_exports/<str:folder_name>/<str:file_name>",
        views.show_html,
        name="html_exports",
    ),
    path("list", GHGList.as_view(), name="ghg"),
    path("update", GHGListUpdate.as_view(), name="update-ghg"),
]
