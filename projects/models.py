from django.db import models
from django.conf import settings
import datetime as dt
# Create your models here.

class Project(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="created_projects", null=False)
    project_leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="leaded_projects", null=True)
    project_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="projects")
    title = models.CharField(max_length=50, null=False)
    description = models.TextField()
    related_skills = models.JSONField()
    difficulty = models.IntegerField()
    start_date = models.DateField(null=True)
    completion_date = models.DateField(null=True)
    deadline = models.DateField()
    active = models.BooleanField(default=True)
    
class Task(models.Model):
    title = models.CharField(max_length=50)
    asignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="tasks", null=False)
    asigner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="asigned_tasks", null=False)
    parent_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_tasks", null=False)
    description = models.TextField()
    deadline = models.DateField(null=True)
    completed = models.BooleanField(default=False)