from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Profile
from .forms import LoginForm, RegisterForm, UserProfileForm
from .decorators import logout_required

# Create your views here.


@logout_required
def login_view(request):

    # If user has filled form and wants to post form
    context = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        context['form'] = form
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            # log user in if authenticated
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('index_page')
            else:
                messages.error(request, 'Email or Password entered incorrect.')

    # Present empty form to user
    else:
        context['form'] = LoginForm()

    return render(request, 'account/login.html', context)


@logout_required
def demo_view(request):
    context = {}
    demo_role = {}
    demo_role['ADMIN'] = 'ADMIN'
    demo_role['DEV'] = 'DEV'
    demo_role['SUB'] = 'SUB'
    demo_role['MAN'] = 'MAN'
    context['role'] = demo_role
    return render(request, 'account/demo_user_login.html', context)


@logout_required
def demo_login_view(request, role):


    # Log user in with demo account
    """ demo_user_password = "demo-password"
    demo_user_email = "demo-user@email.com"
    user = authenticate(request, email=demo_user_email,
                        password=demo_user_password) """
    #login(request, user)

    return redirect('demo_account')

@logout_required
def register_view(request):

    context = {}
    # If user has filled form and wants to post form
    if request.method == "POST":
        form = RegisterForm(request.POST)
        context['form'] = form
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            password_confirm = form.cleaned_data["password_confirm"]
            if password == password_confirm:
                if Account.objects.filter(username=username).exists():
                    messages.error(request, 'Username, ' +
                                   username + ', is already in use.')
                elif Account.objects.filter(email=email).exists():
                    messages.error(request, 'Email, ' +
                                   email + ', is already in use.')
                else:
                    user = Account.objects.create_user(email, username, password)
                    user_profile = Profile.objects.create(user=user, first_name=first_name, last_name=last_name)
                    return redirect('user_profile')
            else:
                messages.error(request, 'Passwords do not match.')

    # Else present empty form to user
    else:
        context['form'] = RegisterForm()

    return render(request, "account/register.html", context)


@login_required(login_url='login_page')
def profile_view(request):

    context = {}
    user = request.user
    # If user has filled form and wants to post form
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = get_object_or_404(Profile, user=user)

            if request.FILES.get('profile_picture', None) is not None:
                image = request.FILES['profile_picture']
                profile.profile_picture = image

            profile.first_name = form.cleaned_data["first_name"]
            profile.last_name = form.cleaned_data["last_name"]
            profile.website = form.cleaned_data["website"]
            profile.address = form.cleaned_data["address"]
            profile.city = form.cleaned_data["city"]
            profile.country = form.cleaned_data["country"]
            profile.save()

            user.username = form.cleaned_data["username"]
            user.save()

            return redirect('user_profile')

    # Else present empty form to user
    else:
        profile = get_object_or_404(Profile, user=user)
        form = UserProfileForm(initial={'username': user.username, 'website': profile.website, 'first_name': profile.first_name,
                                        'last_name': profile.last_name, 'address': profile.address, 'city': profile.city, 'country': profile.country})
        context['user'] = user

        if profile:
            context['form'] = form

    return render(request, "account/profile.html", context)


@login_required(login_url='login_page')
def profile_detail_view(request, slug):
    context = {}
    context['user_profile'] = get_object_or_404(Profile, slug=slug)
    return render(request, "account/profile_detail.html", context)


@login_required(login_url='login_page')
def logout_view(request):
    logout(request)
    return redirect("login_page")
