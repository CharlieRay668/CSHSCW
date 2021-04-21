from django.db import models
from django.conf import settings
import datetime as dt

class School(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="school_logos", blank=True)
    overseer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="overseer_of")
    tech_spec = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="techincal_specialist_of")
    proj_man = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="project_manager_of")
    tut_out = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="tutoring_outreach_of")
    coms = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="communications_of")
    school_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="schools")

    @property
    def safe_img_url(self):
        if self.logo:
            return self.logo.url
        else:
            return "/media/school_logos/default.png"