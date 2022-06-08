from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Room
from .serializers import RoomSer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]

    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all() 
    rooms_ser = RoomSer(rooms, many=True)

    return Response(rooms_ser.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk) 
    room_ser = RoomSer(room, many=False)

    return Response(room_ser.data)