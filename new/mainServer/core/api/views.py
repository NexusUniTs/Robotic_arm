"""
views.py - Central Server API per la comunicazione con il Raspberry Pi
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .virtual_arm import VirtualArmState
from .serializers import JointUpdateSerializer, DeviceAuthSerializer


@api_view(['GET'])
def root_server(request):
    """
    1. Root Endpoint (GET /)
    Restituisce esattamente il messaggio richiesto.
    """
    return Response(
        "welcome to the root, stop tinckering on it like a madman YOU'LL BRAKE IT",
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_arm_status(request):
    """
    2. Endpoint Controllo Stato Oggetto (GET /api/arm/status/)
    Legge lo stato dell'oggetto VirtualArmState gestito in virtual_arm.py.
    """
    arm = VirtualArmState()
    return Response(arm.get_state(), status=status.HTTP_200_OK)


@api_view(['POST'])
def update_arm_joints(request):
    """
    3. Endpoint Input Modifica Joint (POST /api/arm/joints/)
    Riceve i nuovi valori dei joint e li aggiorna nell'oggetto virtuale del braccio.
    """
    serializer = JointUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    arm = VirtualArmState()
    device_id = request.data.get("device_id", "anonymous_device")
    
    # Aggiorna l'oggetto virtuale con i nuovi valori dei 6 joint
    updated_state = arm.update_joints(serializer.validated_data, device_id=device_id)

    return Response({
        "message": "Joint values successfully updated in virtual object.",
        "state": updated_state
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def authenticate_device(request):
    """
    4. Endpoint Autenticazione Dispositivi (POST /api/auth/device/)
    Autentica un dispositivo (Raspberry Pi o Client) verificando id e secret_key.
    """
    serializer = DeviceAuthSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    device_id = serializer.validated_data['device_id']
    secret_key = serializer.validated_data['secret_key']

    if secret_key == "raspberry_pi_secret_key_2026":
        return Response({
            "authenticated": True,
            "device_id": device_id,
            "token": f"token_device_{device_id}_auth_valid",
            "message": "Dispositivo autenticato con successo."
        }, status=status.HTTP_200_OK)
    
    return Response({
        "authenticated": False,
        "message": "Autenticazione fallita: credenziali dispositivo non valide."
    }, status=status.HTTP_401_UNAUTHORIZED)