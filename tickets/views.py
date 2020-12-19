from django.shortcuts import render, get_object_or_404
from account.models import Profile
from projects.models import Project, ProjectRole
from .models import Ticket, TicketComment, TicketAttachment
from index.models import DirectMessage, Alert
# Create your views here.

def tickets_view(request):
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user = user)
    context['user_tickets'] = Ticket.objects.filter(assigned_to = user_profile)
    context['profile'] = user_profile
    context['direct_messages'] = DirectMessage.objects.filter(receiver = user_profile).order_by('-created_on')[:5]
    context['alerts'] = Alert.objects.filter(user = user_profile).order_by('-created_on')[:5]
    return render(request, "tickets/tickets.html", context)