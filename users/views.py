import os

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.utils import timezone

from users.forms import CustomUserCreationForm, CustomUserChangeForm, MessageForm
from users.models import CustomUser


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


@staff_member_required
def admin_panel(request):
    users = CustomUser.objects.all()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            recipient_list = str(post.emails).split(",")
            # send_mail(
            #     post.subject,
            #     post.message,
            #     os.environ.get('EMAIL_HOST_USER'),
            #     recipient_list,
            #     fail_silently=False,
            # )
            email = EmailMessage(
                subject=post.subject,
                body=post.message,
                from_email=os.environ.get('EMAIL_HOST_USER'),
                bcc=recipient_list
            )
            email.send(fail_silently=False)

            messages.success(request, 'Form submission successful')
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = MessageForm()

    return render(request, 'admin_panel/admin_panel.html', {"users": users, 'form': form})
