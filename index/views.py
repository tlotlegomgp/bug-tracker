from operator import attrgetter
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from account.models import Profile
from tickets.models import Ticket, TicketAssignee
from projects.models import Project, ProjectRole
from .models import Todo, Alert, DirectMessage
from .forms import TodoForm


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


def get_user_tickets(user_profile):
    manager_project_roles = ProjectRole.objects.filter(user = user_profile).filter(user_role = "Project Manager")
    submitter_project_roles = ProjectRole.objects.filter(user = user_profile).filter(user_role = "Submitter")
    if user_profile.user.is_admin:
        tickets = Ticket.objects.all().order_by('-created_on')
    elif manager_project_roles or submitter_project_roles:
        tickets = []
        for role in manager_project_roles:
            project_tickets = role.project.tickets.all().order_by('-created_on')
            for ticket in project_tickets:
                tickets.append(ticket)

        for role in submitter_project_roles:
            project_tickets = role.project.tickets.all().order_by('-created_on')
            for ticket in project_tickets:
                if ticket.created_by == user_profile:
                    tickets.append(ticket)


        user_tickets_assignments = TicketAssignee.objects.filter(user=user_profile).order_by('-created_on')
        user_tickets = [assignment.ticket for assignment in user_tickets_assignments]

        for ticket in user_tickets:
            tickets.append(ticket)

        tickets = sorted(list(set(tickets)), key=attrgetter('created_on'), reverse=True)
    else:
        user_tickets_assignments = TicketAssignee.objects.filter(user=user_profile).order_by('-created_on')
        tickets = [assignment.ticket for assignment in user_tickets_assignments]

    
    return tickets


def paginate_list(items, items_per_page, request):
    page = request.GET.get('page', 1)
    items_paginator = Paginator(items, items_per_page)

    try:
        items = items_paginator.page(page)
    except PageNotAnInteger:
        items = items_paginator.page(items_per_page)
    except EmptyPage:
        items = items_paginator.page(items_paginator.num_pages)

    return items


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
        user_tickets = get_user_tickets(user_profile)

        resolved_tickets = 0
        new_tickets = 0
        in_progress_tickets = 0
        total_tickets = 0

        for ticket in user_tickets:
            total_tickets += 1
            if ticket.status == 'RESOLVED':
                resolved_tickets += 1
            elif ticket.status == 'NEW':
                new_tickets += 1
            elif ticket.status == 'IN_PROGRESS':
                in_progress_tickets += 1


        context['total_tickets'] = total_tickets
        if total_tickets != 0:
            context['resolved_tickets'] = round(resolved_tickets*100 / total_tickets)
            context['new_tickets'] = round(new_tickets*100 / total_tickets)
            context['in_progress_tickets'] = round(in_progress_tickets*100 / total_tickets)
        else:
            default_value = round(100/3)
            context['resolved_tickets'] = default_value
            context['new_tickets'] = default_value
            context['in_progress_tickets'] = default_value

        todos_count = Todo.objects.filter(created_by=user_profile).count()
        completed_todos = Todo.objects.filter(created_by=user_profile).filter(status='COM').count()
        if todos_count != 0:
            todos_percentage = round(completed_todos*100 / todos_count)
        else:
            todos_percentage = 0
        context['todos_percentage'] = todos_percentage

        user_todos = Todo.objects.filter(created_by=user_profile).filter(status='SCH').order_by('-created_on')

        user_todos = paginate_list(user_todos, 5, request)

        context['user_todos'] = user_todos

        if user.is_admin:
            context['tickets_count'] = user_tickets.count()
            context['projects_count'] = Project.objects.all().count()

        context['form'] = TodoForm()

        return render(request, "index/dashboard.html", context)


@login_required(login_url='login_page')
def add_todo_view(request):
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.cleaned_data['todo']

            create_todo = Todo.objects.create(created_by = user_profile, note=todo)

        return redirect('index_page')


@login_required(login_url='login_page')
def delete_todo_view(request, id):
    todo = get_object_or_404(Todo, id=id)
    todo.status = 'COM'
    todo.save()
    return redirect('index_page')


@login_required(login_url='login_page')
def clear_alerts_view(request):
    user = request.user
    user_profile = get_object_or_404(Profile, user = user)
    user_alerts = Alert.objects.filter(user = user_profile)

    for alert in user_alerts:
        alert.status = 'READ'
        alert.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='login_page')
def clear_messages_view(request):
    user = request.user
    user_profile = get_object_or_404(Profile, user = user)
    user_messages = DirectMessage.objects.filter(receiver = user_profile)

    for message in user_messages:
        message.status = 'READ'
        message.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



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
