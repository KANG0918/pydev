from django.urls import path

from .views import about, home

app_name = "pages"

urlpatterns = [
    path("about", about, name="about"),
    path("", home, name="root"),
]
