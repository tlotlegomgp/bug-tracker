from django.shortcuts import render, get_object_or_404
from account.models import Profile
from projects.models import Project, ProjectRole
from .models import Ticket, TicketComment, TicketAttachment, TicketAssignee
from .forms import TicketForm
from index.models import DirectMessage, Alert
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login_page')
def tickets_view(request):
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user = user)
    context['user_tickets'] = Ticket.objects.filter(assigned_to = user_profile).order_by('-created_on')
    context['profile'] = user_profile
    context['direct_messages'] = DirectMessage.objects.filter(receiver = user_profile).order_by('-created_on')[:5]
    context['alerts'] = Alert.objects.filter(user = user_profile).order_by('-created_on')[:5]
    return render(request, "tickets/tickets.html", context)



@login_required(login_url='login_page')
def add_ticket_view(request, slug):
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user = user)

    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            status = forms.POST['status']
            class_type = forms.POST['class_type']
            priority = forms.POST['priority']
            description = form.cleaned_data["description"]
            project = get_object_or_404(Project, slug = slug)
            ticket = Ticket.objects.create(title = title, description = description, created_by = user, status = status, priority = priority, class_type = class_type, project = project)
            ticket.save()

            assignees = request.POST.getlist('assignees')
            for member_email in assignees:
                member_account = get_object_or_404(Account, email = member_email)
                member_profile = get_object_or_404(Profile, user = member_account)
                ticket_assignee = TicketAssignee.objects.create(ticket = ticket, user = member_profile)
                ticket_assignee.save()

            return redirect('projects_page')
    #Present empty form to user
    else:
        context['profile'] = user_profile
        context['direct_messages'] = DirectMessage.objects.filter(receiver = user_profile).order_by('-created_on')[:5]
        context['alerts'] = Alert.objects.filter(user = user_profile).order_by('-created_on')[:5]
        context['users'] = Profile.objects.all()
        context['form'] = TicketForm()

    return render(request, "tickets/add_ticket.html", context)