from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import  Profile, Todo, DirectMessage, Alert
from tickets.models import Ticket, TicketComment, TicketAttachment
from projects.models import Project, ProjectRole

# Create your views here.

@login_required(login_url='login_page')
def index_view(request):
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user = user)
    context['profile'] = user_profile
    context['user_tickets'] = Ticket.objects.filter(assigned_to = user_profile)
    context['complete_tickets'] = Ticket.objects.filter(created_by = user_profile).filter(status='RESOLVED')

    if context['user_tickets'].count() != 0:
        context['tickets_percentage'] = round(context['complete_tickets'].count()*100 / context['user_tickets'].count())

    context['user_projects'] = Project.objects.filter(created_by = user_profile)
    context['latest_projects'] = Project.objects.filter(created_by = user_profile).order_by('-created_on')[:5]
    context['user_todos'] = Todo.objects.filter(created_by = user_profile).order_by('-created_on')
    context['direct_messages'] = DirectMessage.objects.filter(receiver = user_profile).order_by('-created_on')[:5]
    context['alerts'] = Alert.objects.filter(user = user_profile).order_by('-created_on')[:5]
    return render(request, "index/dashboard.html", context)


@login_required(login_url='login_page')
def team_view(request):
    context = {}
    return render(request, "index/team.html", context)


@login_required(login_url='login_page')
def handler404(request):
    return render(request, 'index/404.html', status=404)


@login_required(login_url='login_page')
def handler403(request):
    return render(request, 'index/403.html', status=403)


@login_required(login_url='login_page')
def handler400(request):
    return render(request, 'index/400.html', status=400)


@login_required(login_url='login_page')
def handler500(request):
    return render(request, 'index/500.html', status=500)



