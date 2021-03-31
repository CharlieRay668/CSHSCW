from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from users.models import User
from schools.models import School
from .forms import CreateProfile, CreateSkill, UploadImage
from .models import Profile, Skill

def user_profile(response):
    user = response.user
    if hasattr(user, 'profile'):
        profile = user.profile
        return render(response, "profiles/userprofile.html", {"publicuser":user, "hasprofile":True, "haspicture":False})
    else:
        return render(response, "profiles/userprofile.html", {"publicuser":user, "hasprofile":False})

def create_profile(response):
    schools = [school.name for school in School.objects.all()]
    if response.method == "POST":
        form = CreateProfile(response.POST, response.FILES)
        print(form.errors)
        if form.is_valid():
            cleaned = form.cleaned_data
            user = response.user
            try:
                school = School.objects.get(name=cleaned['school'])
            except:
                return render(response, "profiles/create.html", {"form":CreateProfile(), "schools":schools, "error_msg":"Sorry, no school with that name exists. Please select one from the list"})
            grade = cleaned['grade']
            picture = cleaned['picture']
            github = cleaned['github']
            teir = cleaned['teir']
            profile = Profile(user=user, school=school, grade=grade, picture=picture, github=github, teir=teir)
            profile.save()
            user.profile = profile
            return redirect("/profile/")
    else:
        form = CreateProfile()
        return render(response, "profiles/create.html", {"form":form, "schools":schools})

def edit_profile(response):
    return render(response, "profiles/editprofile.html")

def update_profile(response):
    user = response.user
    profile = user.profile
    if response.method == "POST":
        form = UploadImage(response.POST, response.FILES)
        if form.is_valid():
            cleaned = form.cleaned_data
            picture = cleaned['picture']
            profile.picture = picture
            profile.save()
            return redirect("/profile/")
    else:
        school = response.GET.get("school", None)
        grade = response.GET.get("grade", None)
        profile_picture = response.GET.get("profile_picture", None)
        github = response.GET.get("github", None)
        teir = response.GET.get("teir", None)
        bio = response.GET.get("bio", None)
        if school is not None:
            try:
                school = School.objects.get(name=school)
                profile.school = school
            except:
                return HttpResponseBadRequest("User not found")
        if grade is not None:
            profile.grade = grade
        if github is not None:
            profile.github = github
        if teir is not None:
            profile.teir = teir
        if bio is not None:
            profile.bio = bio
        profile.save(update_fields=["school", "grade", "github", "teir", "bio"])
        return HttpResponse("Success")

def add_skill(response):
    context = {}
    form = CreateSkill()
    if response.method == "POST":
        form = CreateSkill(response.POST)
        print(form.errors)
        if form.is_valid():
            cleaned = form.cleaned_data
            user = response.user
            name = cleaned['name']
            length = cleaned['length']
            ability = cleaned['ability']
            skill = Skill(user=user, name=name, length=length, ability=ability)
            skill.save()
            user.skills.add(skill)
            return redirect("/profile/")
    context['form'] = form
    return render(response, "profiles/addskill.html", context)

def view_skill(response, user_id):
    context = {}
    user = User.objects.get(id=user_id)
    skills = user.skills.all()
    context['publicuser'] = user
    context['skills'] = skills
    context['user_is_user'] = response.user.id == user_id
    return render(response, "profiles/viewskill.html", context)

def user_projects(response):
    context ={}
    user = response.user
    context['member_projects'] = user.projects.all()
    context['leader_projects'] = user.leaded_projects.all()
    context['creator_projects'] = user.created_projects.all()
    context['possessive'] = "You"
    return render(response, "profiles/userprojects.html", context)

def public_user_projects(response, user_id):
    context = {}
    user = User.objects.get(id=user_id)
    context['member_projects'] = user.projects.all()
    context['leader_projects'] = user.leaded_projects.all()
    context['creator_projects'] = user.created_projects.all()
    context['possessive'] = "They"
    return render(response, "projects/userprojects.html", context)

def public_profile(response, user_id):
    user = User.objects.get(id=user_id)
    if hasattr(user, 'profile'):
        profile = user.profile
        return render(response, "profiles/publicprofile.html", {"publicuser":user, "hasprofile":True, "haspicture":False})
    else:
        return render(response, "profiles/publicprofile.html", {"publicuser":user, "hasprofile":False})

