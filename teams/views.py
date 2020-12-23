from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.models import Profile

# Create your views here.


@login_required(login_url='login_page')
def team_view(request):
    context = {}
    context['users'] = Profile.objects.all()
    return render(request, "teams/team.html", context)
