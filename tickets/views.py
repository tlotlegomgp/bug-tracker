from operator import attrgetter
from django.shortcuts import render, get_object_or_404, redirect
from account.models import Profile
from projects.models import Project, ProjectRole
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from index.views import get_user_tickets, paginate_list
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
    tickets = get_user_tickets(user_profile)

    if request.GET:
        query = request.GET.get('qs', '')
        context['search'] = query
        if user.is_admin:
            results = tickets.filter(Q(title__icontains=query) | Q(status__icontains=query) | Q(priority__icontains=query) | Q(class_type__icontains=query)).distinct()
        else:
            query = query.lower()
            results = []
            for ticket in tickets:
                if query in {ticket.title.lower(), ticket.status.lower(), ticket.class_type.lower(), ticket.priority.lower()}:
                    results.append(ticket)

        tickets = results


    context['user_tickets'] = paginate_list(tickets, TICKETS_PER_PAGE, request)
    return render(request, "tickets/tickets.html", context)



def can_user_add_ticket(user, project):
    user_profile = get_object_or_404(Profile, user=user)
    sub_role = ProjectRole.objects.filter(project=project).filter(user=user_profile).filter(user_role="Submitter").first()
    man_role = ProjectRole.objects.filter(project=project).filter(user=user_profile).filter(user_role="Project Manager").first()

    return (sub_role is not None) or (man_role is not None) or (user.is_admin)


@login_required(login_url='login_page')
def add_ticket_view(request, slug):

    context = {}
    user = request.user
    project = get_object_or_404(Project, slug=slug)

    if not can_user_add_ticket(user, project):
        raise PermissionDenied


    user_profile = get_object_or_404(Profile, user=user)
    

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
            assignee_id = form.cleaned_data['assignee']
            assigned_user = get_object_or_404(Profile, id=assignee_id)
            ticket_assignee = TicketAssignee.objects.create(ticket=ticket, user=assigned_user)

            return redirect('view_project', slug=slug)
    # Present empty form to user
    else:
        project_roles = ProjectRole.objects.filter(project=project).filter(user_role="Developer").order_by('-created_on')
        form = TicketForm()
        form_assignee_choices = ((role.user.id, role.user.first_name + " " + role.user.last_name) for role in project_roles)
        form.fields['assignee'].choices = form_assignee_choices
        context['form'] = form
        context['project'] = project

    return render(request, "tickets/add_ticket.html", context)


@login_required(login_url='login_page')
def edit_ticket_view(request, slug):
    context = {}
    user = request.user
    ticket = get_object_or_404(Ticket, slug=slug)
    ticket_assignee = get_object_or_404(TicketAssignee, ticket=ticket)
    user_profile = get_object_or_404(Profile, user=user)
    user_project_role = ProjectRole.objects.filter(project=ticket.project).filter(user=user_profile).first()

    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            
            ticket.title = form.cleaned_data["title"]
            ticket.description = form.cleaned_data["description"]
            ticket.status = form.cleaned_data['status']
            ticket.class_type = form.cleaned_data['class_type']
            ticket.priority = form.cleaned_data['priority']
            ticket.save()
            
            if user_project_role and user_project_role.user_role != "Developer" or user.is_admin:
                assignee_id = form.cleaned_data["assignee"]
                assigned_user = get_object_or_404(Profile, id=assignee_id)
                ticket_assignee = get_object_or_404(TicketAssignee, ticket=ticket)

                if not ticket_assignee:
                    new_ticket_assignee = TicketAssignee.objects.create(user=assigned_user, ticket=ticket)
                else:
                    ticket_assignee.user = assigned_user
                    ticket_assignee.save()

            return redirect('tickets_page')
    # Present empty form to user
    else:
        context['user_project_role'] = user_project_role
        context['ticket'] = ticket
        form = TicketForm()

        if user_project_role and user_project_role.user_role == "Developer":
            form.fields['title'].widget.attrs['readonly'] = True
            form.fields['description'].widget.attrs['readonly'] = True
            form.fields['assignee'].widget.attrs['readonly'] = True

        form.initial = {'title': ticket.title, 'description': ticket.description,
                                              'status': ticket.status, 'class_type': ticket.class_type, 'priority': ticket.priority, 'assignee': ticket_assignee.user.id}

        context['form'] = form

    return render(request, "tickets/edit_ticket.html", context)


@login_required(login_url='login_page')
def delete_ticket_view(request, slug):
    if request.user.is_admin:
        ticket = get_object_or_404(Ticket, slug=slug)
        ticket.delete()
        return redirect('tickets_page')
    else:
        raise PermissionDenied


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

            return redirect('view_ticket', slug=slug)

    else:
        context['ticket'] = ticket
        context['ticket_attachments'] = TicketAttachment.objects.filter(ticket=ticket).order_by('-created_on')

        comments = TicketComment.objects.filter(ticket=ticket).order_by('-created_on')

        context['ticket_comments'] = paginate_list(comments, COMMENTS_PER_PAGE, request)
        context['ticket_developer'] = get_object_or_404(TicketAssignee, ticket=ticket).user
        context['submitter'] = ticket.created_by
        context['manager'] = ProjectRole.objects.filter(project=ticket.project).filter(user_role="Project Manager").first().user
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
    if request.user.is_admin:
        attachment = get_object_or_404(TicketAttachment, id=attachment_id)
        ticket_slug = attachment.ticket.slug
        attachment.delete()
        return redirect('view_ticket', slug=ticket_slug)
    else:
        raise PermissionDenied
