from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket, TicketComment, TicketAttachment, Profile, Project, ProjectRole, Todo

# Create your views here.

#@login_required(login_url='login_page')
def index_view(request):
    context = {}
    user = request.user
    context['profile'] = Profile.objects.filter(user = user)
    context['user_tickets'] = Ticket.objects.filter(created_by = user)
    context['user_projects'] = Project.objects.filter(created_by = user)
    return render(request, "index/dashboard.html", context)