from . import views
from django.urls import path

app_name = "resume"  # 因不同app中可能有index、show所以需要作出一個空間


urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>", views.show, name="show"),
]
