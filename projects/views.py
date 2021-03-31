from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from .forms import CreateProject, CreateTask
from .models import Project, Task
from .utils import Utility
from users.models import User

def projects(response):
    projects = Project.objects.all()
    return render(response, "projects/projectview.html", {'projects':projects})

def create_project(response):
    if response.method == "POST":
        form = CreateProject(response.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            user = response.user
            title = cleaned['title']
            description = cleaned['description']
            related_skills = [item.strip() for item in cleaned['related_skills'].split(",")]
            difficulty = cleaned['difficulty']
            deadline = cleaned['deadline']
            project = Project(creator=user, title=title, description=description, related_skills=related_skills, difficulty=difficulty, deadline=deadline)
            project.save()
            user.created_projects.add(project)
            return redirect("/projects/")
    else:
        form = CreateProject()
    return render(response, "projects/create.html", {"form":form})

def create_task(response, project_id):
    context = {}
    project = Project.objects.get(id=project_id)
    users = [user.username for user in project.project_members.all()]
    if project.project_leader.username not in users:
        users.append(project.project_leader.username)
    context['users'] = users
    if response.method == "POST":
        form = CreateTask(response.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            user = response.user
            title = cleaned['title']
            try:
                asignee = User.objects.get(username=cleaned["asignee"])
            except:
                return HttpResponseBadRequest("User not found")
            description = cleaned['description']
            deadline = cleaned['deadline']
            task = Task(title=title, asignee=asignee, asigner=user, parent_project=project, description=description, deadline=deadline)
            task.save()
            return redirect("/projects/"+str(project_id)+"/")
    else:
        form = CreateTask()
    context['form'] = form
    return render(response, "projects/createtask.html", context)
    
def single_project(response, project_id):
    project = Project.objects.get(id=project_id)
    return render(response, "projects/individual_project.html", {'project': project})

def edit_project(response, project_id):
    project = Project.objects.get(id=project_id)
    users = User.objects.all()
    users = [user.username for user in users]
    creator = project.creator
    leader = project.project_leader
    members = project.project_members
    return render(response, "projects/edit.html", {'project': project, "users":users})

def update_project(response, project_id):
    project = Project.objects.get(id=project_id)
    title = response.GET.get("title", None)
    related_skills = response.GET.get("related_skills", None)
    difficulty = response.GET.get("difficulty", None)
    add_leader = response.GET.get("add_project_leader", None)
    add_member = response.GET.get("add_project_member", None)
    remove_leader = response.GET.get("remove_project_leader", None)
    remove_member = response.GET.get("remove_project_member", None)
    description = response.GET.get("description", None)
    active = response.GET.get("active", None)
    print(active)
    if title is not None:
        project.title  = title
    if related_skills is not None:
        project.related_skills = [item.strip() for item in related_skills.split(",")]
    if difficulty is not None:
        project.difficulty = difficulty
    if add_leader is not None:
        try:
            leader = User.objects.get(username=add_leader)
            project.project_leader = leader
        except:
            return HttpResponseBadRequest("User not found")
    if add_member is not None:
        try:
            member = User.objects.get(username=add_member)
            project.project_members.add(member)
        except:
            return HttpResponseBadRequest("User not found")
    if remove_leader is not None:
        project.project_leader = None
    if remove_member is not None:
        try:
            member = User.objects.get(username=remove_member)
            project.project_members.remove(member)
        except:
            return HttpResponseBadRequest("User not found")
    if description is not None:
        project.description = description
    if active is not None:
        project.active = not project.active
    project.save(update_fields=["title", "related_skills", "difficulty", "project_leader", "description", "active"])
    return HttpResponse("Success")

def view_tasks(response, project_id):
    project = Project.objects.get(id=project_id)
    ut = Utility()
    tasks = ut.sort_by_completion(project.project_tasks.all())
    return render(response, "projects/viewtasks.html", {"project":project, "tasks":tasks})

def view_task(response, project_id, task_id):
    task = Task.objects.get(id=task_id)
    project = Project.objects.get(id=project_id)
    delete_task = response.GET.get("delete_task", None)
    if delete_task is not None:
        if delete_task:
            task.delete()
    return render(response, "projects/viewtask.html", {"task":task, "project":project})
