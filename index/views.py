from operator import attrgetter
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from account.models import Profile
from tickets.models import Ticket, TicketAssignee
from projects.models import Project
from .models import Todo


# Search for projects from search bar


def search_projects(query=None):
    qs = []
    queries = query.split(" ")
    for q in queries:
        projects = Project.objects.filter(Q(name__icontains=q)).distinct()

        for project in projects:
            qs.append(project)

    return list(set(qs))

# Search for tickets from search bar


def search_tickets(query=None):
    qs = []
    queries = query.split(" ")
    for q in queries:
        tickets = Ticket.objects.filter(Q(title__icontains=q)).distinct()

        for ticket in tickets:
            qs.append(ticket)

    return list(set(qs))


# Search for users from search bar


def search_users(query=None):
    qs = []
    queries = query.split(" ")
    for q in queries:
        users = Profile.objects.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q)).distinct()

        for user in users:
            qs.append(user)

    return list(set(qs))


# Create your views here.
@login_required(login_url='login_page')
def index_view(request):
    query = ""
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    if request.GET and request.GET.get('q', None):
        query = request.GET.get('q', ' ')
        context['query'] = str(query)
        projects_query = sorted(search_projects(
            query), key=attrgetter('created_on'), reverse=True)
        tickets_query = sorted(search_tickets(
            query), key=attrgetter('created_on'), reverse=True)
        users_query = sorted(search_users(
            query), key=attrgetter('first_name'), reverse=True)
        context['projects'] = projects_query
        context['tickets'] = tickets_query
        context['users'] = users_query
        return render(request, "index/search_results.html", context)

    else:
        if user.is_admin:
            user_tickets = Ticket.objects.all()
            resolved_tickets = Ticket.objects.filter(status='RESOLVED').count()
            new_tickets = Ticket.objects.filter(status='NEW').count()
            in_progress_tickets = Ticket.objects.filter(status='IN_PROGRESS').count()
        else:
            user_tickets = TicketAssignee.objects.filter(user=user_profile)
            resolved_tickets = TicketAssignee.objects.filter(
                user=user_profile).filter(ticket__status='RESOLVED').count()
            new_tickets = TicketAssignee.objects.filter(
                user=user_profile).filter(ticket__status='NEW').count()
            in_progress_tickets = TicketAssignee.objects.filter(
                user=user_profile).filter(ticket__status='IN_PROGRESS').count()

        if user_tickets.count() != 0:
            context['resolved_tickets'] = round(
                resolved_tickets*100 / user_tickets.count())
            context['new_tickets'] = round(
                new_tickets*100 / user_tickets.count())
            context['in_progress_tickets'] = round(
                in_progress_tickets*100 / user_tickets.count())
        else:
            default_value = round(100/3)
            context['resolved_tickets'] = default_value
            context['new_tickets'] = default_value
            context['in_progress_tickets'] = default_value

        user_todos = Todo.objects.filter(created_by=user_profile).order_by('-created_on')
        page = request.GET.get('page', 1)
        todos_paginator = Paginator(user_todos, 5)

        try:
            user_todos = todos_paginator.page(page)
        except PageNotAnInteger:
            user_todos = todos_paginator.page(5)
        except EmptyPage:
            user_todos = todos_paginator.page(todos_paginator.num_pages)

        context['user_todos'] = user_todos

        if user.is_admin:
            context['tickets_count'] = user_tickets.count()
            context['projects_count'] = Project.objects.all().count()

        return render(request, "index/dashboard.html", context)


@login_required(login_url='login_page')
def handler404(request, exception=None):
    return render(request, 'index/404.html', status=404)


@login_required(login_url='login_page')
def handler403(request, exception=None):
    return render(request, 'index/403.html', status=403)


@login_required(login_url='login_page')
def handler400(request, exception=None):
    return render(request, 'index/400.html', status=400)


@login_required(login_url='login_page')
def handler500(request):
    return render(request, 'index/500.html', status=500)
