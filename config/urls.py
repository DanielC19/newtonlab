from django.urls import path, include

urlpatterns = [
    path("", include("src.application.home.urls")),
]
