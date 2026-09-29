from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import RegisterForm
from .models import Profile


def register_view(request):


    if request.user.is_authenticated:
        return redirect('article_list')

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

  
            user = form.save()


            Profile.objects.create(
                user=user,
                role='user'
            )


            login(request, user)

            return redirect('article_list')

    else:

        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect('article_list')

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            profile, created = Profile.objects.get_or_create(
                user=user
            )


            if profile.is_blocked:

                form.add_error(
                    None,
                    'Bu istifadəçi bloklanıb.'
                )

            else:

                login(request, user)

                return redirect('article_list')

    else:

        form = AuthenticationForm()

    return render(
        request,
        'accounts/login.html',
        {
            'form': form
        }
    )


def logout_view(request):

    logout(request)

    return redirect('article_list')