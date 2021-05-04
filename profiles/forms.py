from django import forms
import datetime as dt
from .models import Profile, Skill
from django.utils.safestring import mark_safe

class UploadImage(forms.ModelForm):
    picture = forms.ImageField(label = "Profile Picture", required=False)

    class Meta:
        model = Profile
        fields = ['picture']

class CreateProfile(forms.Form):
    school = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'list':'schools'}))
    grade = forms.ChoiceField(label = "Grade", choices=[(9, "Freshman (9)"),
                                                    (10, "Sophomore (10)"),
                                                    (11, "Junior (11)"),
                                                    (12, "Senior (12)")])
    picture = forms.ImageField(label = "Profile Picture", required=False)
    github = forms.URLField(label= "Link to GitHub Profile", max_length=300)
    teir = forms.ChoiceField(label = "Teir Level", choices=[(0, "Teir 0"),
                                                (1, "Teir 1"),
                                                (2, "Teir 2"),
                                                (3, "Teir 3"),
                                                (4, "Teir 4"),])

class CreateSkill(forms.ModelForm):
    name = forms.CharField(max_length=50, label="Name of skill (Python, Data Manipulation, Pandas)")
    length = forms.CharField(max_length=20, label="How long have you had experience with this skill?")
    ability = forms.ChoiceField(label = "Ability", choices=[(0, "Just Learning"),
                                            (1, "Beginner"),
                                            (2, "Intermediate"),
                                            (3, "Advanced"),
                                            (4, "Very Advanced"),])

    class Meta:
        model = Skill
        fields = ['name', 'length', 'ability']
