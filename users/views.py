from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from . import forms


def login_page(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('quiz:index')
            else:
                messages.error(request, 'Login failed.')

    context = {'form': form}
    return render(request, 'registration/login.html', context)


def logout_user(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form.
        form = forms.SignupForm()
    else:
        # Process completed form.
        form = forms.SignupForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page.
            login(request, new_user)
            return redirect('quiz:index')

        # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)


@api_view(['GET'])
def logout_api(request):
    if not request.user.is_authenticated:
        return Response({"message": "You are not logged in."}, status.HTTP_403_FORBIDDEN)
    request.user.auth_token.delete()
    return Response("logged out!", status.HTTP_200_OK)