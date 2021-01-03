from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.core.exceptions import PermissionDenied
from account.models import Profile
from .forms import UserForm

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


@login_required(login_url='login_page')
def user_management_view(request):

    if not request.user.is_admin:
        raise PermissionDenied


    context = {}
    users = Profile.objects.all().order_by('first_name')

    page = request.GET.get('page', 1)
    users_paginator = Paginator(users, USERS_PER_PAGE)

    try:
        users = users_paginator.page(page)
    except PageNotAnInteger:
        users = users_paginator.page(USERS_PER_PAGE)
    except EmptyPage:
        users = users_paginator.page(users_paginator.num_pages)

    context['users'] = users
    UserFormSet = formset_factory(UserForm, extra=users.paginator.count)
    formset = UserFormSet()
    context['formset'] = formset
    for user, form in zip(users, formset):
        form.initial = {'is_active': user.user.is_active, 'is_staff': user.user.is_staff, 'is_admin': user.user.is_admin}
    context['user_forms'] = zip(users, formset)

    return render(request, "teams/user_management.html", context)


@login_required(login_url='login_page')
def update_user_view(request, slug):

    if not request.user.is_admin:
        raise PermissionDenied
    
    user_profile = get_object_or_404(Profile, slug=slug)
    user = user_profile.user
    UserFormSet = formset_factory(UserForm)

    if request.method == "POST":
        formset = UserFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.has_changed():
                    user.is_active = form.cleaned_data['is_active']
                    user.is_staff = form.cleaned_data['is_staff']
                    user.is_admin = form.cleaned_data['is_admin']
                    user.save()

    return redirect('user_management')
