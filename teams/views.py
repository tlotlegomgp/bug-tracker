from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from account.models import Profile

# Create your views here.

USERS_PER_PAGE = 10


@login_required(login_url='login_page')
def team_view(request):
    users = Profile.objects.all().order_by('first_name')
    page = request.GET.get('page', 1)
    users_paginator = Paginator(users, USERS_PER_PAGE)

    try:
        users = users_paginator.page(page)
    except PageNotAnInteger:
        users = users_paginator.page(USERS_PER_PAGE)
    except EmptyPage:
        users = users_paginator.page(users_paginator.num_pages)

    context = {}
    context['users'] = users
    return render(request, "teams/team.html", context)
