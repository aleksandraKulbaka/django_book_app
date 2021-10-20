from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (
    UserRegisterForm, 
    ProfileUpdateForm, 
    UserUpdateForm,
    InterestUpdateForm)
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        b_form = InterestUpdateForm(request.POST, instance=request.user.book_interests)
        if u_form.is_valid() and p_form.is_valid and b_form.is_valid():
            u_form.save()
            p_form.save()
            b_form.save()
            messages.success(request, f'Profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        b_form = InterestUpdateForm(instance=request.user.book_interests)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'b_form': b_form,
    }

    return render(request, 'users/profile.html', context)
    