from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models import Profile, Account
from tickets.models import Ticket
from .models import Project, ProjectRole
from .forms import ProjectForm

# Create your views here.


@login_required(login_url='login_page')
def projects_view(request):
    context = {}
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    context['user_projects'] = Project.objects.filter(
        created_by=profile).order_by('-created_on')

    return render(request, "projects/projects.html", context)


@login_required(login_url='login_page')
def add_project_view(request):
    context = {}
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            project = Project.objects.create(
                name=name, description=description, created_by=user_profile)
            project.save()

            selected_user_id = form.cleaned_data['manager']
            print(selected_user_id)
            selected_user_profile = get_object_or_404(Profile, id=selected_user_id)
            project_role = ProjectRole.objects.create(user=selected_user_profile, project=project, user_role='MAN')
            project_role.save()

            return redirect('projects_page')
    # Present empty form to user
    else:
        context['users'] = Profile.objects.all()
        context['form'] = ProjectForm(initial={'manager': (0, 'Select Project Manager')})

    return render(request, "projects/add_project.html", context)


@login_required(login_url='login_page')
def project_detail_view(request, slug):
    context = {}
    project = get_object_or_404(Project, slug=slug)
    context['user_roles'] = ProjectRole.objects.filter(project=project)
    context['tickets'] = Ticket.objects.filter(
        project=project).order_by('-created_on')
    context['project'] = project

    return render(request, "projects/project_detail.html", context)


@login_required(login_url='login_page')
def delete_project_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    project.delete()
    return redirect('projects_page')


@login_required(login_url='login_page')
def edit_project_view(request, slug):
    context = {}
    project = get_object_or_404(Project, slug=slug)
    current_project_manager = ProjectRole.objects.filter(project=project).filter(user_role='MAN').first()

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
            selected_user_role = ProjectRole.objects.filter(project=project).filter(user_role='MAN').filter(user=selected_user_profile).first()

            if not selected_user_role:
                current_project_manager.delete()
                new_project_manager = ProjectRole.objects.create(user=selected_user_profile, project=project, user_role='MAN')
                new_project_manager.save()

            return redirect('projects_page')
    # Present empty form to user
    else:
        context['users'] = Profile.objects.all()
        context['project'] = project
        context['form'] = ProjectForm(initial={'name': project.name, 'description': project.description,
                                               'manager': current_project_manager.user.id})

    return render(request, "projects/edit_project.html", context)
