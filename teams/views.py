from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models import Profile

# Create your views here.

@login_required(login_url='login_page')
def team_view(request):
    context = {}
    context['users'] = Profile.objects.all()
    return render(request, "teams/team.html", context)