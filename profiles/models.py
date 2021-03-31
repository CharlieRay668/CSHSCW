from django.db import models
from django.conf import settings
from schools.models import School
import datetime as dt

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, related_name="students", null=True)
    grade = models.IntegerField()
    picture = models.ImageField(upload_to="profile_picture", blank=True)
    github = models.URLField(max_length=300)
    teir = models.IntegerField()
    bio = models.TextField()

    @property
    def safe_img_url(self):
        if self.picture:
            return self.picture.url
        else:
            return "/media/profile_picture/defaultprofile.jpg"

class Skill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=50)
    length = models.CharField(max_length=20)
    ability = models.IntegerField()
    