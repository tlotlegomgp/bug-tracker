from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectRole
from index.models import Profile, Ticket

# Create your views here.

@login_required(login_url='login_page')
def projects_view(request):
    context = {}
    user = request.user
    profile = get_object_or_404(Profile, user = user)
    context['user_projects'] = Project.objects.filter(created_by = profile)

    return render(request, "projects/projects.html", context)