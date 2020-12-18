from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectRole

# Create your views here.

@login_required(login_url='login_page')
def projects_view(request):
    context = {}
    return render(request, "index/projects.html", context)