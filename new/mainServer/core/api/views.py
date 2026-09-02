from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def api_root(request):
    return Response('Welcome to the API root! pls stop tinkering it like a madman, you are going to break it')

@api_view(['GET'])
def getVirtualPosition(request):
    return Response('0, 0, 0, 0, 0, 0')

@api_view(['POST'])
def setVirtualPosition(request, movement):
    # transfer wanted movemnt to managemt obj
    return Response('Position updated!')


