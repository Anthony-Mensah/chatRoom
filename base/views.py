from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib.auth.models import User

# Create your views here.

# HOME PAGE
def home(request):
    # SEARCH PARAMETER
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # ROOMS QUERY
    rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)
    )
    # TOPICS QUERY
    topics = Topic.objects.all()
    # MESSAGE QUERY
    all_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    room_count = rooms.count()

    # CONTEXT DIC
    context = {
    'topics':topics,
    'rooms':rooms,
    'all_messages':all_messages,
    'room_count':room_count
    }
    return render(request, 'base/home.html', context)


# ROOM
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = Message.objects.filter(room=room)

    if request.method == 'POST':
        room_message = Message.objects.create(
        user = request.user,
        room = room,
        body = request.POST.get('body')
        )
        room.participants.add(request.user)

    room_participants = room.participants.all()

    # CONTEXT DIC
    context = {
    'room':room,
    'room_messages':room_messages,
    'room_participants':room_participants
    }
    return render(request, 'base/room.html', context)

# USER PROFILE PAGE
def profilePage(request, pk):

    user = User.objects.get(id=pk)
    rooms = Room.objects.filter(host=user)
    topics = Topic.objects.all()
    all_messages = Message.objects.filter(user=user)

    context = {
    'user':user,
    'topics':topics,
    'rooms':rooms,
    'all_messages':all_messages
    }
    return render(request, 'base/profile.html', context)

# ACTIVITY PAGE
def activityPage(request):
    all_messages = Message.objects.all()[0:4]

    context = {
    'all_messages':all_messages
    }
    return render(request, 'base/activity.html',context)

# TOPIC PAGE
def topicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)

    context = {
    'topics':topics
    }
    return render(request, 'base/topic.html',context)


#CRUD CRUD CRUD CRUD CRUD CRUD CRUD CRUD CRUD CRUD

# CREATE ROOM
@login_required(login_url='login')
def createRoom(request):
    room_form = RoomForm()
    topics = Topic.objects.all()
    host = request.user

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
        host = host,
        topic = topic,
        name = request.POST.get('name'),
        description = request.POST.get('description')
        )
        return redirect('home')

    context = {
    'room_form':room_form,
    'topics':topics
    }
    return render(request, 'base/room_form.html', context)

# UPDATE ROOM
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    room_form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    # if request.method == 'POST':
    #     room_form = RoomForm(request.POST,instance=room)
    #     room_form.save()
    #     return redirect('room', pk=room.id)

    context = {
    'room_form':room_form,
    'room':room
    }
    return render(request, 'base/room_form.html', context)

#DELETE ROOM
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You're not allowed here")

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {
    'obj':room
    }
    return render(request, 'base/delete.html',context)

#DELETE MESSAGE
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You're not allowed here")

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context = {
    'obj':message
    }
    return render(request, 'base/delete.html',context)
