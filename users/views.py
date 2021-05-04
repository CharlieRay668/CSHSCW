from django.shortcuts import render
from .models import User

# Create your views here.
def view_users(response):
    users = User.objects.all()
    return render(response, "users/users.html", {'users':users})