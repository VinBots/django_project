from django.urls import path
from . import views
from .views import GHGList, GHGListCreate, GHGListUpdate

urlpatterns = [
    path("<str:corp_name>/", views.corporates_search, name="corporates_search"),
    path("", views.corporates_home, name="corporates_home"),
    path(
        "charts/html_exports/<str:folder_name>/<str:file_name>",
        views.show_html,
        name="html_exports",
    ),
    path("ghg/view/", GHGList.as_view(), name="ghg"),
    path("ghg/update/<int:pk>/", GHGListUpdate.as_view(), name="update-ghg"),
    path("ghg/create/", GHGListCreate.as_view(), name="create-ghg"),
]
