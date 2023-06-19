import re
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from base.models import Room, Topic, User
from .forms import RoomForm

# Create your views here.

def login_page(request: HttpRequest):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password does not exist")
    
    context={}
    return render(request, 'base/login_register.html', context)

def logout_user(request: HttpRequest):
    logout(request)
    return redirect('home')

def home(request: HttpRequest):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q))

    topics = Topic.objects.all()

    context = {"rooms": rooms, "topics": topics, "room_count": rooms.count()}
    return render(request, 'base/home.html', context)

def room(request: HttpRequest, pk: str):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def create_room(request: HttpRequest):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def update_room(request: HttpRequest, pk: str):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_+form.html', context)

def delete_room(request: HttpRequest, pk: str):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':    
        room.delete()
        return redirect('home')
    
    context = {'obj': room}
    return render(request, 'base/delete.html', context)


