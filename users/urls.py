from django.urls import path

from . import views

app_name = "users"  # 因不同app中可能有index、show所以需要作出一個空間


urlpatterns = [
    path("", views.index, name="index"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("sign_out", views.sign_out, name="sign_out"),
    path("register", views.register, name="register"),
]
