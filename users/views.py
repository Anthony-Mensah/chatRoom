from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import MyUserCreationForm, ProfileForm,UpdateUserForm
from django.contrib import messages

# Create your views here.

# REGISTER
def register(request):
    u_form = MyUserCreationForm()

    if request.method == 'POST':
        u_form = MyUserCreationForm(request.POST)
        if u_form.is_valid():
            u_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Account registered for {username}')
            return redirect('login')
        else:
            messages.error(request, 'Error occured while registering')


    context = {
    'u_form':u_form
    }
    return render(request, 'users/register.html', context)

# LOGIN
def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password doesn't exists")


    return render(request, 'users/login.html')

# LOGOUT
def logoutPage(request):
    logout(request)
    return redirect('home')

# UPDATE User
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    u_form = UpdateUserForm(instance=user)
    p_form = ProfileForm(instance=user.profile)

    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST,instance=user)
        p_form = ProfileForm(request.POST,request.FILES,instance=user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('home')#TO BE CHANGED TO PROFILE PAGE

    context = {
    'u_form':u_form,
    'p_form':p_form
    }
    return render(request, 'users/update_user.html', context)

# def profile(request, pk):
#     user = User.objects.get(id=pk)
#
#     context = {
#     'user':user
#     }
#     return redirect(request, 'users/profile.html', context)
