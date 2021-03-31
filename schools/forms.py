from django import forms
import datetime as dt
from .models import School
from django.utils.safestring import mark_safe

class CreateSchool(forms.ModelForm):
    name = forms.CharField(max_length=50)
    logo = forms.ImageField(label = "School Logo", required=False)
    class Meta:
        model = School
        fields = ['name', 'logo']