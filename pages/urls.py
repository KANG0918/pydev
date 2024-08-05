from .views import about, home
from django.urls import path

app_name = "pages"

urlpatterns = [
    path("about", about, name="about"),
    path("", home, name="root"),
]
