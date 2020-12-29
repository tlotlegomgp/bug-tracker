from django.shortcuts import render, get_object_or_404, redirect
from account.models import Profile
from projects.models import Project, ProjectRole
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Ticket, TicketAssignee, TicketComment, TicketAttachment
from .forms import TicketForm, TicketCommentForm, TicketAttachmentForm


TICKETS_PER_PAGE = 10
COMMENTS_PER_PAGE = 8
# Create your views here.


@login_required(login_url='login_page')
def tickets_view(request):
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    user_tickets_assignments = TicketAssignee.objects.filter(user=user_profile).order_by('-created_on')
    tickets = [assignment.ticket for assignment in user_tickets_assignments]

    page = request.GET.get('page', 1)
    tickets_paginator = Paginator(tickets, TICKETS_PER_PAGE)

    try:
        tickets = tickets_paginator.page(page)
    except PageNotAnInteger:
        tickets = tickets_paginator.page(TICKETS_PER_PAGE)
    except EmptyPage:
        tickets = tickets_paginator.page(tickets.num_pages)
    context['user_tickets'] = tickets
    return render(request, "tickets/tickets.html", context)


@login_required(login_url='login_page')
def add_ticket_view(request, slug):
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    project = get_object_or_404(Project, slug=slug)

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

            assignee_id = form.cleaned_data['assignee']
            user_role = form.cleaned_data['user_role']
            assigned_user = get_object_or_404(Profile, id=assignee_id)
            ticket_assignee = TicketAssignee.objects.create(ticket=ticket, user=assigned_user, user_role=user_role)
            ticket_assignee.save()

            return redirect('view_project', slug=slug)
    # Present empty form to user
    else:
        project_roles = ProjectRole.objects.filter(project=project).order_by('-created_on')
        users = [user.user for user in project_roles]
        form = TicketForm()
        form.fields['assignee'].choices = ((u.id, u.first_name + " " + u.last_name) for u in users)
        context['form'] = form
        context['project'] = project

    return render(request, "tickets/add_ticket.html", context)


@login_required(login_url='login_page')
def edit_ticket_view(request, slug):
    context = {}
    ticket = get_object_or_404(Ticket, slug=slug)
    ticket_assignee = get_object_or_404(TicketAssignee, ticket=ticket)
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

            assignee_id = form.cleaned_data["assignee"]
            user_role = form.cleaned_data["user_role"]
            assigned_user = get_object_or_404(Profile, id=assignee_id)
            ticket_assignee = get_object_or_404(TicketAssignee, ticket=ticket)

            if not ticket_assignee:
                new_ticket_assignee = TicketAssignee.objects.create(user=assigned_user, ticket=ticket, user_role=user_role)
            else:
                ticket_assignee.user = assigned_user
                ticket_assignee.user_role = user_role
                ticket_assignee.save()

            return redirect('tickets_page')
    # Present empty form to user
    else:
        context['ticket'] = ticket
        context['form'] = TicketForm(initial={'title': ticket.title, 'description': ticket.description,
                                              'status': ticket.status, 'class_type': ticket.class_type, 'priority': ticket.priority, 'assignee': ticket_assignee.user.id, 'user_role': ticket_assignee.user_role})

    return render(request, "tickets/edit_ticket.html", context)


@login_required(login_url='login_page')
def delete_ticket_view(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug)
    ticket.delete()
    return redirect('tickets_page')


@login_required(login_url='login_page')
def ticket_detail_view(request, slug):
    context = {}
    ticket = get_object_or_404(Ticket, slug=slug)
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        form = TicketCommentForm(request.POST)
        if form.is_valid():
            comment_body = form.cleaned_data['comment']

            ticket_comment = TicketComment.objects.create(user=user_profile, body_message=comment_body, ticket=ticket)
            ticket_comment.save()

            return redirect('view_ticket', slug=slug)

    else:
        context['ticket'] = ticket
        context['ticket_attachments'] = TicketAttachment.objects.filter(ticket=ticket).order_by('-created_on')

        comments = TicketComment.objects.filter(ticket=ticket).order_by('-created_on')

        page = request.GET.get('page', 1)
        comments_paginator = Paginator(comments, COMMENTS_PER_PAGE)

        try:
            comments = comments_paginator.page(page)
        except PageNotAnInteger:
            comments = comments_paginator.page(COMMENTS_PER_PAGE)
        except EmptyPage:
            comments = comments_paginator.page(comments_paginator.num_pages)

        context['ticket_comments'] = comments
        context['form'] = TicketCommentForm()
        context['attachment_form'] = TicketAttachmentForm()

    return render(request, "tickets/ticket_detail.html", context)


@login_required(login_url='login_page')
def ticket_attachment_view(request, slug):
    if request.method == "POST":
        form = TicketAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user_profile = get_object_or_404(Profile, user=user)
            ticket = get_object_or_404(Ticket, slug=slug)

            note = form.cleaned_data['note']
            attachment = request.FILES['attachment']

            new_attachment = TicketAttachment.objects.create(user=user_profile, ticket=ticket, note=note, attachment=attachment)

    return redirect('view_ticket', slug=slug)


@login_required(login_url='login_page')
def delete_attachment_view(request, attachment_id):
    attachment = get_object_or_404(TicketAttachment, id=attachment_id)
    ticket_slug = attachment.ticket.slug
    attachment.delete()
    return redirect('view_ticket', slug=ticket_slug)
