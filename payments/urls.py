from django.urls import path

from . import views

app_name = "payments"  # 因不同app中可能有index、show所以需要作出一個空間


urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
]
