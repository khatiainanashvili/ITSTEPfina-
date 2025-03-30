from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
import logging
from .forms import RegistrationForm

logger = logging.getLogger(__name__)

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})



def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                logger.warning(f'Login failed for username: {username}')
                return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})



def logout_user(request):
    logout(request)
    return redirect('home')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'authentication/password_change.html', {'form': form})

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request, email_template_name='registration/reset_password_email.html')
            return HttpResponse('Reset Email Sent Successfully. Please Check Your Email To Finish The Process')
    else:
        form = PasswordResetForm()
    return render(request, 'authentication/password_reset.html', {'form': form})

def reset_password_confirm(request, uidb64, token):
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=user_id)
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user=user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, user)
                    return HttpResponse('Password reset successful!')
            else:
                form = SetPasswordForm(user=user)
        else:
            return HttpResponse('Invalid Token')
    except (User.DoesNotExist, ValueError, TypeError):
        return HttpResponse('Invalid Credentials')
    return render(request, 'authentication/password_reset_confirm.html', {'form': form})
