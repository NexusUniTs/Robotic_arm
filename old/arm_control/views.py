import time
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Server State Memory
SERVER_STATE = {
    'current_telemetry': {
        'joints': {'j1': 0, 'j2': 0, 'j3': 0, 'j4': 0, 'j5': 0, 'j6': 0},
        'status': {'voltage': 24.4, 'temperature': 35.0, 'torque': 0.0}
    },
    'target_joints': {'j1': 142, 'j2': -45, 'j3': 88, 'j4': 12, 'j5': 0, 'j6': 180},
    'gripper': False,
    'emergency_stop': False,
    'last_seen': 0.0
}

def dashboard(request):
    return render(request, 'dashboard.html')

def monitoring(request):
    return render(request, 'monitoring.html')

@api_view(['POST'])
def pi_sync(request):
    """ Called by the Raspberry Pi to post its true state and fetch latest targets """
    global SERVER_STATE
    data = request.data
    
    # Update last seen timestamp
    SERVER_STATE['last_seen'] = time.time()
    
    if 'joints' in data:
        SERVER_STATE['current_telemetry']['joints'].update(data['joints'])
    if 'status' in data:
        SERVER_STATE['current_telemetry']['status'].update(data['status'])
        
    return Response({
        'target_joints': SERVER_STATE['target_joints'],
        'gripper': SERVER_STATE['gripper'],
        'emergency_stop': SERVER_STATE['emergency_stop']
    })

@api_view(['GET', 'POST'])
def dashboard_sync(request):
    """ Called by the Dashboard UI to push commands and get Pi telemetry """
    global SERVER_STATE
    
    if request.method == 'POST':
        data = request.data
        if 'target_joints' in data:
            SERVER_STATE['target_joints'].update(data['target_joints'])
        if 'gripper' in data:
            SERVER_STATE['gripper'] = data['gripper']
        if 'emergency_stop' in data:
            SERVER_STATE['emergency_stop'] = data['emergency_stop']
            
    # Calculate connection validity (Pi posts every 1s, so >3s means disconnected)
    pi_connected = (time.time() - SERVER_STATE['last_seen']) < 3.0
            
    response_data = dict(SERVER_STATE)
    response_data['pi_connected'] = pi_connected
    
    return Response(response_data)

