from django import forms
import datetime as dt
from .models import Project, Task
from django.utils.safestring import mark_safe

class CreateProject(forms.ModelForm):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    related_skills = forms.CharField(label=mark_safe("Related Skills<br/>Enter as comma seperated values, ex (Python, Data Processing, HTML)"), widget=forms.Textarea)
    difficulty = forms.ChoiceField(label = "Difficulty", choices=[(1, "Very Easy"),
                                                        (2, "Easy"),
                                                        (3, "Medium"),
                                                        (4, "Hard"),
                                                        (5, "Very Hard")])
    deadline = forms.DateField(label=mark_safe("Deadline<br/>Enter as MM/DD/YY"))
    class Meta:
        model = Project
        fields = ['title', 'description', 'related_skills', 'difficulty']

class CreateTask(forms.Form):
    title = forms.CharField(max_length=50)
    asignee = forms.CharField(label="Assign task to:", max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    deadline = forms.DateField(label=mark_safe("Deadline<br/>Enter as MM/DD/YY"))