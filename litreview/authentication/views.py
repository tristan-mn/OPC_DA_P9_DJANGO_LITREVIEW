from django.shortcuts import render, redirect
from authentication import forms
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
# Create your views here.

def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user  =  authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'], 
            )
            if user is not None:
                login(request, user)
                message = f'bonjour, {user.username} vous êtes connêcté.'
            else:
                message = 'identifiants ou mot de passe invalide'
    return render(request, 'authentication/login.html', context={'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(
        request, 'authentication/signup.html', context={'form': form}
    )