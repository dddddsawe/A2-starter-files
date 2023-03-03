from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponseBadRequest
from .models import User

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile_view')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile_view.html'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'password']
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('profile_view')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        password1 = form.cleaned_data.get('password')
        password2 = form.cleaned_data.get('password2')
        email = form.cleaned_data.get('email')

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            return HttpResponseBadRequest("Enter a valid email address")

        # Validate password
        if password1:
            if len(password1) < 8:
                return HttpResponseBadRequest("This password is too short. It must contain at least 8 characters")
            if password1 != password2:
                return HttpResponseBadRequest("The two password fields didn't match")

        return super().form_valid(form)