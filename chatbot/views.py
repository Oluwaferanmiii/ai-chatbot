from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message, ChatSession
from .forms import MessageForm
from django.utils import timezone
from .bot import get_bot_response
from .hf_bot import ask_bot_huggingface
from django.http import HttpResponseRedirect
from django.urls import reverse


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


# @login_required
# def dashboard(request):
#     user = request.user
#     messages = Message.objects.filter(user=user).order_by('timestamp')
#     form = MessageForm()

#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             user_message = form.cleaned_data['content']

#             # Save user message
#             Message.objects.create(
#                 sender='user',
#                 content=user_message,
#                 timestamp=timezone.now(),
#                 user=user
#             )

#             # bot_response = get_bot_response(user_message) (Openai bot response)
#             bot_response = ask_bot_huggingface(user_message)
#             Message.objects.create(
#                 sender='bot',
#                 content=bot_response,
#                 timestamp=timezone.now(),
#                 user=user
#             )

#             return redirect('dashboard')  # Refresh to show new messages

#     return render(request, 'chatbot/dashboard.html', {
#         'messages': messages,
#         'form': form
#     })

def dashboard(request):
    user = request.user
    session_id = request.GET.get('session_id')

    # If session_id is passed, get it. Else, None (used to conditionally show "Start a chat")
    session = None
    messages = []
    if session_id:
        session = get_object_or_404(ChatSession, id=session_id, user=user)
        messages = Message.objects.filter(
            session=session).order_by('timestamp')

    sessions = ChatSession.objects.filter(user=user).order_by('-created_at')

    return render(request, 'chatbot/dashboard.html', {
        'sessions': sessions,
        'messages': messages,
        'current_session': session
    })


@login_required
def new_chat(request):
    session = ChatSession.objects.create(user=request.user)
    return redirect(f"{reverse('dashboard')}?session_id={session.id}")


@login_required
def send_message(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        user_message = request.POST.get('message')

        if session_id and user_message:
            session = get_object_or_404(
                ChatSession, id=session_id, user=request.user)

            # Save user message
            Message.objects.create(
                sender='user',
                content=user_message,
                user=request.user,
                session=session
            )

            # Get bot response
            bot_response = ask_bot_huggingface(user_message)

            Message.objects.create(
                sender='bot',
                content=bot_response,
                user=request.user,
                session=session
            )

        return redirect(f"{reverse('dashboard')}?session_id={session_id}")
