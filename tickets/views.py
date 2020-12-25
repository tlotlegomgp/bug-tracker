from django.shortcuts import render, get_object_or_404, redirect
from account.models import Profile, Account
from projects.models import Project, ProjectRole
from django.contrib.auth.decorators import login_required
from .models import Ticket, TicketAssignee
from .forms import TicketForm, TicketCommentForm


# Create your views here.


@login_required(login_url='login_page')
def tickets_view(request):
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    user_tickets_assignments = TicketAssignee.objects.filter(user=user_profile).order_by('-created_on')
    context['user_tickets'] = [assignment.ticket for assignment in user_tickets_assignments]
    return render(request, "tickets/tickets.html", context)


@login_required(login_url='login_page')
def add_ticket_view(request, slug):
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    project = get_object_or_404(Project, slug=slug)
    context['project'] = project

    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            status = form.cleaned_data['status']
            class_type = form.cleaned_data['class_type']
            priority = form.cleaned_data['priority']
            description = form.cleaned_data["description"]

            ticket = Ticket.objects.create(title=title, description=description, created_by=user_profile,
                                           status=status, priority=priority, class_type=class_type, project=project)
            ticket.save()

            assignees = request.POST.getlist('assignees')
            for member_email in assignees:
                member_account = get_object_or_404(Account, email=member_email)
                member_profile = get_object_or_404(
                    Profile, user=member_account)
                ticket_assignee = TicketAssignee.objects.create(
                    ticket=ticket, user=member_profile)
                ticket_assignee.save()

            return redirect('view_project', slug=slug)
    # Present empty form to user
    else:
        context['users'] = Profile.objects.all()
        context['form'] = TicketForm()

    return render(request, "tickets/add_ticket.html", context)


@login_required(login_url='login_page')
def edit_ticket_view(request, slug):
    context = {}
    ticket = get_object_or_404(Ticket, slug=slug)
    ticket_assignees = TicketAssignee.objects.filter(ticket=ticket)
    assigned_users = [assignment.user for assignment in ticket_assignees]
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            status = form.cleaned_data['status']
            class_type = form.cleaned_data['class_type']
            priority = form.cleaned_data['priority']
            description = form.cleaned_data["description"]

            ticket.title = title
            ticket.description = description
            ticket.status = status
            ticket.class_type = class_type
            ticket.priority = priority
            ticket.save()

            assignees = request.POST.getlist('assignees')
            if not assignees:
                for assignee in ticket_assignees:
                    assignee.delete()

            for member_email in assignees:
                member_account = get_object_or_404(Account, email=member_email)
                member_profile = get_object_or_404(
                    Profile, user=member_account)
                ticket_assignee = TicketAssignee.objects.filter(user=member_profile).filter(ticket=ticket)

                # If user already assigned to ticket
                if ticket_assignee:
                    # If previously assigned user is no longer selected as assgined
                    if ticket_assignee.first() not in ticket_assignees:
                        ticket_assignee.delete()

                # Assign selected user to ticket
                else:
                    new_ticket_assignee = TicketAssignee.objects.create(ticket=ticket, user=member_profile)
                    new_ticket_assignee.save()

            return redirect('tickets_page')
    # Present empty form to user
    else:
        context['assigned_users'] = assigned_users
        context['ticket'] = ticket
        context['users'] = Profile.objects.all()
        context['form'] = TicketForm(initial={'title': ticket.title, 'description': ticket.description,
                                              'status': ticket.status, 'class_type': ticket.class_type, 'priority': ticket.priority})

    return render(request, "tickets/edit_ticket.html", context)


@login_required(login_url='login_page')
def delete_ticket_view(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug)
    ticket.delete()
    return redirect('tickets_page')


@login_required(login_url='login_page')
def ticket_detail_view(request, slug):
    context = {}
    context['ticket'] = get_object_or_404(Ticket, slug=slug)
    context['form'] = TicketCommentForm()
    return render(request, "tickets/ticket_detail.html", context)
