from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_profile, name="user_profile"),
    path("create/", views.create_profile, name="create"),
    path("edit/", views.edit_profile, name="edit"),
    path("update/", views.update_profile, name="update"),
    path("projects/", views.user_projects, name="user_projects"),
    path("addskill/", views.add_skill, name="add_skill"),
    path("<int:user_id>/viewskill/", views.view_skill, name="view_skills"),
    path("<int:user_id>/projects/", views.public_user_projects, name="public_user_projects"), 
    path("<int:user_id>/", views.public_profile, name="public_profile"),
]