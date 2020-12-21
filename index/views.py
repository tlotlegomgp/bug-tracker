from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models import Profile
from .models import Todo, DirectMessage, Alert
from tickets.models import Ticket, TicketComment, TicketAttachment, TicketAssignee
from projects.models import Project, ProjectRole
from django.db.models import Q
from operator import attrgetter 

#Search for projects from search bar
def search_projects(query=None):
	qs = []
	queries = query.split(" ")
	for q in queries:
		projects = Project.objects.filter(Q(name__icontains=q)).distinct()

		for project in projects:
			qs.append(project)

	return list(set(qs))

#Search for tickets from search bar
def search_tickets(query=None):
	qs = []
	queries = query.split(" ")
	for q in queries:
		tickets = Ticket.objects.filter(Q(title__icontains=q)).distinct()

		for ticket in tickets:
			qs.append(ticket)

	return list(set(qs))


def search_users(query=None):
	qs = []
	queries = query.split(" ")
	for q in queries:
		users = Profile.objects.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q)).distinct()

		for user in users:
			qs.append(user)

	return list(set(qs))

# Create your views here.

@login_required(login_url='login_page')
def index_view(request):
    query = ""
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user = user)
    context['profile'] = user_profile

    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)
        projects_query = sorted(search_projects(query), key=attrgetter('created_on'), reverse = True)
        tickets_query = sorted(search_tickets(query), key=attrgetter('created_on'), reverse = True)
        users_query = sorted(search_users(query), key=attrgetter('first_name'), reverse = True)
        context['projects'] = projects_query
        context['tickets'] = tickets_query
        context['users'] = users_query
        return render(request, "index/search_results.html", context)
    
    else:
        user_tickets = TicketAssignee.objects.filter(user = user_profile)
        context['user_tickets'] = user_tickets
        resolved_tickets = TicketAssignee.objects.filter(user = user_profile).filter(ticket__status='RESOLVED').count()
        new_tickets = TicketAssignee.objects.filter(user = user_profile).filter(ticket__status='NEW').count()
        in_progress_tickets = TicketAssignee.objects.filter(user = user_profile).filter(ticket__status='IN_PROGRESS').count()

        if user_tickets.count() != 0:
            context['resolved_tickets'] = round(resolved_tickets*100 / user_tickets.count())
            context['new_tickets'] = round(new_tickets*100 / user_tickets.count())
            context['in_progress_tickets'] = round(in_progress_tickets*100 / user_tickets.count())

        else:
            default_value = round(100/3)
            context['resolved_tickets'] = default_value
            context['new_tickets'] = default_value
            context['in_progress_tickets'] = default_value

        context['user_projects'] = Project.objects.filter(created_by = user_profile)
        context['user_todos'] = Todo.objects.filter(created_by = user_profile).order_by('-created_on')
        context['direct_messages'] = DirectMessage.objects.filter(receiver = user_profile).order_by('-created_on')[:5]
        context['alerts'] = Alert.objects.filter(user = user_profile).order_by('-created_on')[:5]
        return render(request, "index/dashboard.html", context)



@login_required(login_url='login_page')
def handler404(request, exception=None):
    context = {}
    user_profile = request.user
    context['profile'] = get_object_or_404(Profile, user = user_profile)
    return render(request, 'index/404.html', context, status=404)


@login_required(login_url='login_page')
def handler403(request, exception=None):
    context = {}
    user_profile = request.user
    context['profile'] = get_object_or_404(Profile, user = user_profile)
    return render(request, 'index/403.html', context, status=403)


@login_required(login_url='login_page')
def handler400(request, exception=None):
    context = {}
    user_profile = request.user
    context['profile'] = get_object_or_404(Profile, user = user_profile)
    return render(request, 'index/400.html', context, status=400)


@login_required(login_url='login_page')
def handler500(request):
    context = {}
    user_profile = request.user
    context['profile'] = get_object_or_404(Profile, user = user_profile)
    return render(request, 'index/500.html', context, status=500)



