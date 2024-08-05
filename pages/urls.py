from .views import about, home
from django.urls import path


urlpatterns = [
    path("about", about),
    path("", home),
]
