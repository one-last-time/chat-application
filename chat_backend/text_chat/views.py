from django.shortcuts import render


def index(request):
    return render(request, 'text_chat/index.html')


def room(request, room_name):
    return render(request, "text_chat/room.html", {"room_name": room_name})
