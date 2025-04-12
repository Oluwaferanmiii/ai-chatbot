from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message
from .forms import MessageForm
from django.utils import timezone


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Registration successful! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'chatbot/register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'chatbot/login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    messages = Message.objects.filter(user=user).order_by('timestamp')
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            user_message = form.cleaned_data['content']

            # Save user message
            Message.objects.create(
                sender='user',
                content=user_message,
                timestamp=timezone.now(),
                user=user
            )

            # Placeholder bot logic (we’ll improve this soon!)
            bot_response = "This is a dummy bot reply. I'll get smarter later 😄"
            Message.objects.create(
                sender='bot',
                content=bot_response,
                timestamp=timezone.now(),
                user=user
            )

            return redirect('dashboard')  # Refresh to show new messages

    return render(request, 'chatbot/dashboard.html', {
        'messages': messages,
        'form': form
    })
