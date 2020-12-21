from django.shortcuts import render, get_object_or_404
from account.models import Profile
from projects.models import Project, ProjectRole
from .models import Ticket, TicketComment, TicketAttachment
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
def add_ticket_view(request):
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user = user)

    if request.method == "POST":
        form = TicketForm(request.POST)
        """ if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            project = Project.objects.create(name = name, description = description, created_by = user_profile)
            project.save()

            members = request.POST.getlist('members')
            for member_email in members:
                member_account = get_object_or_404(Account, email = member_email)
                member_profile = get_object_or_404(Profile, user = member_account)
                project_role = ProjectRole.objects.create(user = member_profile, project = project)
                project_role.save()

            return redirect('projects_page') """
    #Present empty form to user
    else:
        context['profile'] = user_profile
        context['direct_messages'] = DirectMessage.objects.filter(receiver = user_profile).order_by('-created_on')[:5]
        context['alerts'] = Alert.objects.filter(user = user_profile).order_by('-created_on')[:5]
        context['users'] = Profile.objects.all()
        context['form'] = TicketForm()

    return render(request, "tickets/add_ticket.html", context)