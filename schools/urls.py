from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_school, name="create_school"),
    path("", views.schools, name="schools"),
    path("<int:school_id>/", views.view, name="view"),
    path("<int:school_id>/edit/", views.edit, name="edit"),
    path("<int:school_id>/update/", views.update_school, name="update"),
    path("<int:school_id>/viewmembers/", views.view_members, name="view_members"),
]