from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models import Profile
from index.models import DirectMessage, Alert
from tickets.models import Ticket, TicketComment, TicketAttachment
from projects.models import Project, ProjectRole

# Create your views here.

@login_required(login_url='login_page')
def team_view(request):
    context = {}
    user_profile = get_object_or_404(Profile, user = request.user)
    context['users'] = Profile.objects.all()
    context['profile'] = user_profile
    context['direct_messages'] = DirectMessage.objects.filter(receiver = user_profile).order_by('-created_on')[:5]
    context['alerts'] = Alert.objects.filter(user = user_profile).order_by('-created_on')[:5]
    return render(request, "teams/team.html", context)