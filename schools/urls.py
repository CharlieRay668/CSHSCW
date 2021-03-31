from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_school, name="create_school"),
    path("", views.schools, name="schools"),
]