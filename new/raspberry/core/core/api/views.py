"""
views.py - Application API per Controllo Braccio Robotico 6-DOF su Raspberry Pi

Implementazione basata su Function-Based Views (FBV) con decoratore @api_view.

3 Endpoint principali:
1. root_api (GET /) -> Root endpoint e stato API
2. start_communication (POST /api/connect/) -> Inizio comunicazione con Raspberry Pi
3. set_virtual_position (POST /api/transition/) -> Imposta la posizione virtuale dei 6 vincoli con feedback
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import JointStateSerializer, ConnectRequestSerializer
from .arm_controller import RoboticArmController


@api_view(['GET'])
def root_api(request):
    """
    1. Root Endpoint (GET /)
    Fornisce informazioni generali sull'API, stato della connessione Raspberry Pi 
    ed elenco degli endpoint disponibili.
    """
    controller = RoboticArmController()
    return Response({
        "system": "Raspberry Pi 6-DOF Robotic Arm API",
        "status": "online",
        "hardware_connected": controller.is_connected,
        "endpoints": {
            "root": "/",
            "connect": "/api/connect/",
            "transition": "/api/transition/"
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def start_communication(request):
    """
    2. Endpoint Inizio Comunicazione (POST /api/connect/)
    Inizializza la comunicazione hardware con il Raspberry Pi per abilitare i 6 vincoli.
    """
    serializer = ConnectRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    baudrate = serializer.validated_data.get("baudrate", 115200)
    controller = RoboticArmController()
    success = controller.connect(baudrate=baudrate)

    if success:
        return Response({
            "connected": True,
            "message": "Comunicazione con Raspberry Pi avviata con successo.",
            "current_state": controller.get_current_state()
        }, status=status.HTTP_200_OK)
    
    return Response({
        "connected": False,
        "message": "Impossibile stabilire la comunicazione con il Raspberry Pi."
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def set_virtual_position(request, movement=None):
    """
    3. Endpoint Feedback Transizione di Stato / Impostazione Posizione Virtuale (POST /api/transition/)
    Usa lo standard con decoratore @api_view(['POST']) e gestisce il parametro `movement`.
    Riceve i 6 vincoli del braccio e trasferisce il movimento desiderato all'oggetto controller.

    Risposta:
    - SUCCESSO: Restituisce booleano true {"success": True, "message": "Position updated!", ...}
    - FALLIMENTO: Restituisce booleano false ed il JSON dello stato CORRENTE dei 6 vincoli.
    """
    payload = movement if movement is not None else request.data
    serializer = JointStateSerializer(data=payload)
    
    controller = RoboticArmController()

    if not serializer.is_valid():
        return Response({
            "success": False,
            "current_state": controller.get_current_state(),
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    target_state = serializer.validated_data

    # Trasferimento del movimento desiderato all'oggetto di gestione controller
    success, error_msg = controller.execute_transition(target_state)

    if success:
        return Response({
            "success": True,
            "message": "Position updated!",
            "new_state": controller.get_current_state()
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "success": False,
            "current_state": controller.get_current_state(),
            "error": error_msg
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


# ==============================================================================
# ENDPOINT AGGIUNTIVI OPZIONALI (FUNCTION-BASED VIEWS COMMENTATE)
# ==============================================================================

# @api_view(['GET'])
# def get_arm_state(request):
#     """[Opzionale] Legge lo stato corrente dei 6 vincoli senza effettuare movimenti."""
#     controller = RoboticArmController()
#     return Response({
#         "is_connected": controller.is_connected,
#         "current_state": controller.get_current_state()
#     }, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def emergency_stop(request):
#     """[Opzionale] Arresto immediato di emergenza ed interruzione alimentazione motori."""
#     controller = RoboticArmController()
#     controller.is_connected = False
#     return Response({
#         "emergency_stop": True,
#         "message": "Arresto di emergenza attivato. Motori disabilitati.",
#         "current_state": controller.get_current_state()
#     }, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def calibrate_arm(request):
#     """[Opzionale] Routine di calibrazione/homing dei 6 vincoli."""
#     controller = RoboticArmController()
#     home_state = {"j1": 0.0, "j2": 0.0, "j3": 0.0, "j4": 0.0, "j5": 0.0, "j6": 0.0}
#     controller.current_state = home_state
#     return Response({
#         "calibrated": True,
#         "message": "Procedura di homing completata.",
#         "current_state": home_state
#     }, status=status.HTTP_200_OK)