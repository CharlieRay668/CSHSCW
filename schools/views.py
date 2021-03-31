from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from .forms import CreateSchool
from .models import School
from users.models import User

def schools(response):
    schools = School.objects.all()
    return render(response, "schools/view.html", {'schools':schools})

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

