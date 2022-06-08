from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from .models import *
from .forms import RoomForm, UserForm

def home_view (request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    #rooms = Room.objects.filter(topic__name__icontains = q)
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) | #podría usar el & para AND
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )

    context ={
        'rooms': rooms, 
        'topics': topics, 
        'room_count': room_count,
        'room_messages': room_messages
        }
    return render(request,'base/home.html', context)

def room_view (request, pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all()
    #Se pueden traer los hijos, poniendo el nombre en minuscula con el "_set"
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
        }

    return render(request,'base/room.html', context)

def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics
        }

    return render (request, 'base/profile.html', context)

@login_required(login_url="/login")
def room_create(request):
    form = RoomForm()
    topics = Topic.objects.all()

    context = {
        'form': form,
        'topics': topics
        }

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        #Previamente estaba el form.isvalid, habría que ver si es conveniente dejarlo así
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect ('home')
    return render (request, 'base/room_form.html', context)

@login_required(login_url="/login")
def room_update(request, pk):
    room = Room.objects.get (id = pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    context = {
        'form': form,
        'topics': topics,
        'room': room
        }

    if request.user != room.host:
        messages.error(request, f'{request.user.username.capitalize()} is not allowed to update room "{ room }"')
        return redirect ('home')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect ('home')

    return render (request, 'base/room_form.html', context)

@login_required(login_url='login')
def room_delete(request, pk):
    room = Room.objects.get (id=pk)
    context = {'obj': room}

    if request.user != room.host:
        messages.error(request, f'{request.user.username.capitalize()} is not allowed to delete room "{ room }"')
        return redirect ('home')

    if request.method == 'POST':
        room.delete()
        return redirect ('home')

    return render (request, 'base/delete.html', context)

def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect ('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User and password do not match')

    context = {'page': page}

    return render (request, "base/login_register.html", context)

def register_page(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Something was wrong during registration")

    context = {'page': page, 'form': form}

    return render (request, "base/login_register.html", context)

def logout_page(request):
    logout(request)

    return redirect ('home')

@login_required(login_url='login')
def message_delete(request, pk):
    message = Message.objects.get (id=pk)
    context = {'obj': message}

    if request.user != message.user:
        messages.error(request, f'{request.user.username.capitalize()} is not allowed to delete message "{message}"')
        return redirect ('home')

    if request.method == 'POST':
        message.delete()
        return redirect ('room', pk = message.room.id)

    return render (request, 'base/delete.html', context)

login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    context = {'form': form}

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)

        if form.is_valid:
            form.save()

            return redirect ('user-profile', pk=user.id)

    return render (request, 'base/update-user.html', context)

def topics_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)
    room_count = Room.objects.all().count

    context = {
        'topics': topics,
        'room_count': room_count
        }

    return render (request, 'base/topics.html', context)

def activity_view(request):
    room_messages = Message.objects.all().order_by('-created')[:10][::-1]

    context = {
        'room_messages': room_messages,
        }

    return render (request, 'base/activity.html', context)