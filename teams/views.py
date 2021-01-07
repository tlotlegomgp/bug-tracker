from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from account.models import Profile
from index.models import DirectMessage, Conversation
from .forms import UserForm, MessageForm

# Create your views here.

USERS_PER_PAGE = 10


@login_required(login_url='login_page')
def team_view(request):
    users = Profile.objects.all().order_by('first_name')

    context = {}
    if request.GET:
        query = request.GET.get('qs', '')
        context['search'] = query
        results = users.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query)).distinct()
        users = results


    page = request.GET.get('page', 1)
    users_paginator = Paginator(users, USERS_PER_PAGE)

    try:
        users = users_paginator.page(page)
    except PageNotAnInteger:
        users = users_paginator.page(USERS_PER_PAGE)
    except EmptyPage:
        users = users_paginator.page(users_paginator.num_pages)

    context['users'] = users
    context['form'] = MessageForm()
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



@login_required(login_url='login_page')
def send_message_view(request, user_id):

     if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            recipient = get_object_or_404(Profile, id=user_id)
            user = request.user
            author = get_object_or_404(Profile, user = user)

            conversation = Conversation.objects.filter(Q(user_1=author) | Q(user_2=author)).filter(Q(user_1=recipient) | Q(user_2=recipient)).first()
            if not conversation:
                conversation = Conversation.objects.create(user_1= author, user_2=recipient)
            
            direct_message = DirectMessage.objects.create(author=author, receiver=recipient, body=message, conversation=conversation)