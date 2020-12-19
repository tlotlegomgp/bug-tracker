from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectRole
from account.models import Profile
from index.models import DirectMessage, Alert
from tickets.models import Ticket

# Create your views here.

@login_required(login_url='login_page')
def projects_view(request):
    context = {}
    user = request.user
    profile = get_object_or_404(Profile, user = user)
    context['user_projects'] = Project.objects.filter(created_by = profile)
    context['profile'] = profile
    context['direct_messages'] = DirectMessage.objects.filter(receiver = profile).order_by('-created_on')[:5]
    context['alerts'] = Alert.objects.filter(user = profile).order_by('-created_on')[:5]

    return render(request, "projects/projects.html", context)