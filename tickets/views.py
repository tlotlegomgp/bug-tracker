from django.shortcuts import render, get_object_or_404, redirect
from account.models import Profile, Account
from projects.models import Project, ProjectRole
from .models import Ticket, TicketComment, TicketAttachment, TicketAssignee
from .forms import TicketForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login_page')
def tickets_view(request):
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user = user)
    context['user_tickets'] = TicketAssignee.objects.filter(user = user_profile).order_by('-created_on')
    return render(request, "tickets/tickets.html", context)



@login_required(login_url='login_page')
def add_ticket_view(request, slug):
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user = user)
    project = get_object_or_404(Project, slug = slug)
    context['project'] = project

    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            status = form.cleaned_data['status']
            class_type = form.cleaned_data['class_type']
            priority = form.cleaned_data['priority']
            description = form.cleaned_data["description"]
            
            ticket = Ticket.objects.create(title = title, description = description, created_by = user_profile, status = status, priority = priority, class_type = class_type, project = project)
            ticket.save()

            assignees = request.POST.getlist('assignees')
            for member_email in assignees:
                member_account = get_object_or_404(Account, email = member_email)
                member_profile = get_object_or_404(Profile, user = member_account)
                ticket_assignee = TicketAssignee.objects.create(ticket = ticket, user = member_profile)
                ticket_assignee.save()

            return redirect('view_project', slug=slug)
    #Present empty form to user
    else:
        context['users'] = Profile.objects.all()
        context['form'] = TicketForm()

    return render(request, "tickets/add_ticket.html", context)