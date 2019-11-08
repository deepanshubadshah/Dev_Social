from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def search_user(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''

    users_list = User.objects.filter(username__contains=search_text)

    return render_to_response('users/profile_search.html', {'users_list' : users_list})



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)           ##with current logged in user as an instance
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)  ##with the current user's profile as an instance
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)           ##with current logged in user as an instance
        p_form = ProfileUpdateForm(instance=request.user.profile)  ##with the current user's profile as an instance
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
