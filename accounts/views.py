from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .forms import RegistrationForm, EditProfileForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = AuthenticationForm


class CustomLogoutView(LogoutView):
    next_page = 'home'


@login_required
def view_profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'accounts/profile.html', context=context)


class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = RegistrationForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user


class EditProfileView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        user = self.request.user
        user.email = form.cleaned_data['email']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        return super().form_valid(form)

    def get_initial(self):
        user = self.request.user
        return {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
