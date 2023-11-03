from django.shortcuts import render, redirect
from .forms import UserAppForm, LoginForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.template import loader
from django.http import HttpResponse, HttpResponseForbidden
from profiles.models import Profile
from profiles.forms import EditProfile
from .forms import EditUser
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserAppForm(data = request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            Profile.objects.create(user = new_user)
            redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = UserAppForm()
    return render(request, 'user/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect('course:index')
            else:
                return HttpResponse("Authentication failed")
    else:
        form = LoginForm()
    context = {"form": form}
    return render(request, 'user/login.html', context)
    


def edit(request):
    if request.method == 'POST':
        editprofile = EditProfile(instance=request.user, data = request.POST)
        edituser = EditUser(instance=request.user.profile, data = request.POST)
        if editprofile.is_valid() and edituser.is_valid():
            edituser.save()
            editprofile.save()
            return HttpResponse('success')
    else:
        editprofile = EditProfile(instance=request.user)
        edituser = EditUser(instance=request.user.profile)
    return render(request, 'user/edit.html', {'editprofile': editprofile, 'edituser': edituser})
@login_required
def index(request):
    print(request.user.is_superuser)
    if not request.user.is_superuser:
        return HttpResponseForbidden("Vous n'avez pas acces à ces données")
    else:
        list_user = User.objects.all()
        return render(request, 'user/list_user.html', {'list_user': list_user})