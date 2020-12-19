from django.shortcuts import render, get_object_or_404
from account.models import Profile
from projects.models import Project, ProjectRole
from .models import Ticket, TicketComment, TicketAttachment
# Create your views here.

def tickets_view(request):
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user = user)
    context['user_tickets'] = Ticket.objects.filter(assigned_to = user_profile)
    return render(request, "tickets/tickets.html", context)