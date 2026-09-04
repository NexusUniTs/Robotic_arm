"""
views.py - Application API per Controllo Braccio Robotico 6-DOF su Raspberry Pi

Architettura minimale basata su 3 endpoint principali:
1. RootAPIView (GET /) -> Informazioni e stato generale dell'API
2. ConnectAPIView (POST /api/connect/) -> Avvio della comunicazione con Raspberry Pi
3. TransitionAPIView (POST /api/transition/) -> Transizione di stato dei 6 vincoli e feedback su successo/fallimento

In coda al file sono stati inclusi come commenti gli endpoint aggiuntivi raccomandati per estensioni future.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import JointStateSerializer, ConnectRequestSerializer
from .arm_controller import RoboticArmController


class RootAPIView(APIView):
    """
    1. Root Endpoint (GET /)
    Fornisce informazioni generali sull'API, stato della connessione Raspberry Pi 
    ed elenco degli endpoint disponibili nel sistema.
    """
    def get(self, request):
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


class ConnectAPIView(APIView):
    """
    2. Endpoint Inizio Comunicazione (POST /api/connect/)
    Inizializza la comunicazione hardware con il Raspberry Pi, 
    abilitando il controllo sui 6 vincoli del braccio.
    """
    def post(self, request):
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


class TransitionAPIView(APIView):
    """
    3. Endpoint Feedback Transizione di Stato (POST /api/transition/)
    Riceve in formato JSON la configurazione desiderata dei 6 vincoli (j1..j6).
    
    Risposta:
    - In caso di SUCCESSO: Restituisce booleano true {"success": True, "message": "..."}
    - In caso di FALLIMENTO: Restituisce booleano false ed il JSON dello stato CORRENTE del braccio.
    """
    def post(self, request):
        serializer = JointStateSerializer(data=request.data)
        if not serializer.is_valid():
            controller = RoboticArmController()
            return Response({
                "success": False,
                "current_state": controller.get_current_state(),
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        target_state = serializer.validated_data
        controller = RoboticArmController()

        # Esecuzione della transizione di stato sui 6 vincoli
        success, error_msg = controller.execute_transition(target_state)

        if success:
            # Se la transizione riesce, restituisce esito positivo booleano (True)
            return Response({
                "success": True,
                "message": "Transizione di stato dei 6 vincoli completata con successo.",
                "new_state": controller.get_current_state()
            }, status=status.HTTP_200_OK)
        else:
            # Se fallisce, restituisce booleano False ed il JSON dello stato attuale del braccio
            return Response({
                "success": False,
                "current_state": controller.get_current_state(),
                "error": error_msg
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


