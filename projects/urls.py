from django.urls import path
from . import views

urlpatterns = [
    path("", views.projects, name="projectlist"),
    path("<int:project_id>/", views.single_project, name="view"),
    path("<int:project_id>/edit/", views.edit_project, name="edit"),
    path("<int:project_id>/update/", views.update_project, name="update"),
    path("<int:project_id>/addtask/", views.create_task, name="add_task"),
    path("<int:project_id>/viewtasks/", views.view_tasks, name="view_tasks"),
    path("<int:project_id>/viewtasks/<int:task_id>/", views.view_task, name="view_task"),
    path("create/", views.create_project, name="create"),
]