from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from .forms import CreateSchool
from .models import School
from users.models import User

def schools(response):
    schools = School.objects.all()
    return render(response, "schools/view.html", {'schools':schools})

def view(response, school_id):
    school = School.objects.get(id=school_id)
    return render(response, "schools/viewschool.html", {'school':school})

def view_members(response, school_id):
    school = School.objects.get(id=school_id)
    return render(response, "schools/viewmembers.html", {'school':school})

def edit(response, school_id):
    school = School.objects.get(id=school_id)
    users = User.objects.all()
    users = [user.username for user in users]
    return render(response, "schools/edit.html", {'school': school, "users":users})

def update_school(response, school_id):
    school = School.objects.get(id=school_id)
    name = response.GET.get("name", None)
    overseer = response.GET.get("add_overseer", None)
    tech_spec = response.GET.get("add_tech_spec", None)
    proj_man = response.GET.get("add_proj_man", None)
    tut_out = response.GET.get("add_tut_out", None)
    coms = response.GET.get("add_coms", None)
    add_member = response.GET.get("add_school_member", None)
    remove_overseer = response.GET.get("remove_overseer", None)
    remove_tech_spec = response.GET.get("remove_tech_spec", None)
    remove_proj_man = response.GET.get("remove_proj_man", None)
    remove_tut_out = response.GET.get("remove_tut_out", None)
    remove_coms = response.GET.get("remove_coms", None)
    remove_member = response.GET.get("remove_school_member", None)
    if name is not None:
        school.name = name
    if overseer is not None:
        try:
            overseer = User.objects.get(username=overseer)
            school.overseer = overseer
        except:
            return HttpResponseBadRequest("User not found")
    if tech_spec is not None:
        print(tech_spec)
        try:
            tech_spec = User.objects.get(username=tech_spec)
            school.tech_spec = tech_spec
        except:
            return HttpResponseBadRequest("User not found")
    if proj_man is not None:
        try:
            proj_man = User.objects.get(username=proj_man)
            school.proj_man = proj_man
        except:
            return HttpResponseBadRequest("User not found")
    if tut_out is not None:
        try:
            tut_out = User.objects.get(username=tut_out)
            school.tut_out = tut_out
        except:
            return HttpResponseBadRequest("User not found")
    if coms is not None:
        try:
            coms = User.objects.get(username=coms)
            school.coms = coms
        except:
            return HttpResponseBadRequest("User not found")
    if add_member is not None:
        try:
            member = User.objects.get(username=add_member)
            school.school_members.add(member)
        except:
            return HttpResponseBadRequest("User not found")
    if remove_overseer is not None:
        school.overseer = None
    if remove_tech_spec is not None:
        school.tech_spec = None
    if remove_proj_man is not None:
        school.proj_man = None
    if remove_tut_out is not None:
        school.tut_out = None
    if remove_coms is not None:
        school.coms = None
    if remove_member is not None:
        try:
            member = User.objects.get(username=remove_member)
            school.school_members.remove(member)
        except:
            return HttpResponseBadRequest("User not found")
    school.save(update_fields=["name", "overseer", "tech_spec", "proj_man", "tut_out", "coms"])
    return HttpResponse("Success")

def create_school(response):
    if response.method == "POST":
        form = CreateSchool(response.POST, response.FILES)
        if form.is_valid():
            cleaned = form.cleaned_data
            user = response.user
            name = cleaned['name']
            logo = cleaned['logo']
            school = School(name=name, logo=logo)
            school.save()
            return redirect("/schools/")
    else:
        form = CreateSchool()
    return render(response, "schools/create.html", {"form":form})

