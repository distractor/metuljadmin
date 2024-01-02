from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from metuljadmin import settings
from users.forms import CustomUserCreationForm, CustomUserChangeForm


@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='/accounts/login/')
def user_edit(request):
    args = {}

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submission successful')
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = CustomUserChangeForm(instance=request.user)


    args['form'] = form
    return render(request, 'users/profile_show.html', args)


def user_new(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('/')
        else:
            return render(request, 'users/create.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/create.html', {'form': form})
