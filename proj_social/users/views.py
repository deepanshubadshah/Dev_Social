from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import Friend
from post import views as postviews


def register(request, *args, **kwargs):
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
    if (request.method == "POST"):
        search_text = request.POST['search_text']
        if(search_text != ''):
            users_list = (User.objects.filter(username__contains=search_text))|(User.objects.filter(profile__name__contains=search_text))
        else:
            users_list = ''
    else:
        users_list = ''

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

def connections(request):
    frlist_exist = Friend.objects.filter(current_user=request.user).exists()
    if frlist_exist:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
    else:
        friends = ''
    context = {
        'friends': friends,
    }
    return render(request, 'users/connections.html', context)

@login_required
def send_connect(request, operation, pk):
    new_person = User.objects.get(pk=pk)
    new_users_username = new_person.username
    if(operation == 'add'):
        Friend.make_friend(request.user, new_person)
        return redirect(postviews.UserPostListView, username=new_users_username)
    elif(operation == 'remove'):
        Friend.remove_friend(request.user, new_person)
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
        messages.success(request, 'Connection removed successfully!')
        return redirect(connections)
