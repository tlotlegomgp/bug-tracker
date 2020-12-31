from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from account.models import Profile
from .models import Project, ProjectRole
from .forms import ProjectForm, ProjectRolesForm

# Create your views here.

PROJECTS_PER_PAGE = 10
USERS_PER_PAGE = 5


@login_required(login_url='login_page')
def projects_view(request):
    context = {}
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    project_roles = ProjectRole.objects.filter(user=profile).order_by('-created_on')
    projects = [role.project for role in project_roles]

    page = request.GET.get('page', 1)
    projects_paginator = Paginator(projects, PROJECTS_PER_PAGE)

    try:
        projects = projects_paginator.page(page)
    except PageNotAnInteger:
        projects = projects_paginator.page(PROJECTS_PER_PAGE)
    except EmptyPage:
        projects = projects_paginator.page(projects_paginator.num_pages)

    context['user_projects'] = projects

    return render(request, "projects/projects.html", context)


@login_required(login_url='login_page')
def add_project_view(request):
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        form = ProjectForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            project = Project.objects.create(
                name=name, description=description, created_by=user_profile)

            selected_user_id = form.cleaned_data['manager']
            selected_user_profile = get_object_or_404(Profile, id=selected_user_id)
            project_role = ProjectRole.objects.create(user=selected_user_profile, project=project, user_role='Project Manager')

            members = form.cleaned_data.get("members")
            for member_id in members:
                member = get_object_or_404(Profile, id=member_id)

                if selected_user_profile != member:
                    project_role = ProjectRole.objects.create(user=member, project=project)

            return redirect('manage_roles', slug=project.slug)
    # Present empty form to user
    else:
        form = ProjectForm(request.POST or None)
        context['form'] = form
    return render(request, "projects/add_project.html", context)


@login_required(login_url='login_page')
def project_detail_view(request, slug):
    context = {}

    project = get_object_or_404(Project, slug=slug)
    context['project'] = project

    users = ProjectRole.objects.filter(project=project).order_by('-created_on')
    page = request.GET.get('page', 1)
    users_paginator = Paginator(users, USERS_PER_PAGE)

    try:
        users = users_paginator.page(page)
    except PageNotAnInteger:
        users = users_paginator.page(USERS_PER_PAGE)
    except EmptyPage:
        users = users_paginator.page(users_paginator.num_pages)

    tickets = project.tickets.all().order_by('-created_on')

    context['tickets'] = tickets
    context['user_roles'] = users

    return render(request, "projects/project_detail.html", context)


@login_required(login_url='login_page')
def project_roles_view(request, slug):
    context = {}
    project = get_object_or_404(Project, slug=slug)
    context['project'] = project

    if request.method == "POST":
        print("Its POST")
        form = ProjectRolesForm(request.POST or None)
        context['form'] = form
        if form.is_valid():
            print("Its VALID")
            role = form.cleaned_data['role']

            members = form.cleaned_data.get("members")
            for member_id in members:
                user = get_object_or_404(Profile, id=member_id)
                member_role = ProjectRole.objects.filter(user=user).filter(project=project).first()
                member_role.user_role = role
                member_role.save()

            return redirect('manage_roles', slug=project.slug)

    else:
        project_roles = ProjectRole.objects.filter(project=project).exclude(user_role="Project Manager").order_by('-created_on')
        form_member_choices = ((role.user.id, role.user.first_name + " " + role.user.last_name) for role in project_roles)
        form = ProjectRolesForm()
        form.fields['members'].choices = form_member_choices

        page = request.GET.get('page', 1)
        users_paginator = Paginator(project_roles, 6)

        try:
            project_roles = users_paginator.page(page)
        except PageNotAnInteger:
            project_roles = users_paginator.page(USERS_PER_PAGE)
        except EmptyPage:
            project_roles = users_paginator.page(users_paginator.num_pages)

        context['user_roles'] = project_roles

        context['form'] = form

    return render(request, "projects/assign_roles.html", context)


@login_required(login_url='login_page')
def delete_project_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    project.delete()
    return redirect('projects_page')


@login_required(login_url='login_page')
def edit_project_view(request, slug):
    context = {}
    project = get_object_or_404(Project, slug=slug)
    current_project_manager = ProjectRole.objects.filter(project=project).filter(user_role='Project Manager').first()
    current_user_roles = ProjectRole.objects.filter(project=project)
    user_ids = [user.user.id for user in current_user_roles]

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]

            project.name = name
            project.description = description
            project.save()

            selected_user_id = form.cleaned_data['manager']
            selected_user_profile = get_object_or_404(Profile, id=selected_user_id)
            selected_user_role = ProjectRole.objects.filter(project=project).filter(
                user_role='Project Manager').filter(user=selected_user_profile).first()

            if not selected_user_role:
                current_project_manager.delete()
                new_project_manager = ProjectRole.objects.create(user=selected_user_profile, project=project, user_role='Project Manager')

            members = form.cleaned_data.get("members")

            for member_id in members:
                member_profile = get_object_or_404(Profile, id=member_id)
                member_role = ProjectRole.objects.filter(user=member_profile, project=project).first()
                if not member_role:
                    project_role = ProjectRole.objects.create(user=member_profile, project=project, user_role='Member')

            for user_role in current_user_roles:
                if str(user_role.user.id) not in members and user_role.user.id != current_project_manager.user.id:
                    user_role.delete()

            return redirect('projects_page')
    # Present empty form to user
    else:
        context['project'] = project
        context['form'] = ProjectForm(initial={'name': project.name, 'description': project.description,
                                               'manager': current_project_manager.user.id, 'members': user_ids})

    return render(request, "projects/edit_project.html", context)
