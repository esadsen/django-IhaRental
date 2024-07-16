from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../login/')
    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form})


def logoutUser(request):
    logout(request)
    messages.success(request,"Logged out")
    return redirect("index")