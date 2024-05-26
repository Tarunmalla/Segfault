from django.shortcuts import render,redirect
from django.db.models import Q
# Create your views here.
from django.http import HttpResponse
from .models import Room,Topic
from .forms import RoomForm
# rooms=[
#     {'id':1,'name':"Leetcode Doubts"},
#     {'id':2,'name':"Lets start Networking"},
#     {'id':3,'name':"Django applications"},
# ]
def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics=Topic.objects.all()
    room_count=rooms.count()
    context={'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request,'core/home.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    context={'room':room}
    return render(request,'core/room.html',context)

def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'core/room_form.html',context)

def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')
        
    context={'form':form}
    return render(request,'core/room_form.html',context) 

def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'core/delete.html',{'obj':room})