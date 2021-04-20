from django.db import models
from django.conf import settings
import datetime as dt

class School(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="school_logos", blank=True)
    leaders = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="school_lead")

    @property
    def safe_img_url(self):
        if self.logo:
            return self.logo.url
        else:
            return "/media/school_logos/default.png"