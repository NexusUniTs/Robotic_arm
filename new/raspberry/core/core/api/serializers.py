"""
serializers.py - Serializers DRF per il Braccio Robotico 6-DOF su Raspberry Pi
"""

from rest_framework import serializers


class JointStateSerializer(serializers.Serializer):
    """
    Serializer per la validazione dei 6 vincoli/giunti del braccio robotico.
    I 6 vincoli sono gestiti come valori numerici floating-point in un oggetto JSON:
    
    JSON di esempio in ingresso:
    {
        "j1": 45.0,
        "j2": -15.5,
        "j3": 90.0,
        "j4": 0.0,
        "j5": 30.2,
        "j6": 180.0
    }
    """
    j1 = serializers.FloatField(help_text="Angolo Vincolo 1 (Base / Rotazione)")
    j2 = serializers.FloatField(help_text="Angolo Vincolo 2 (Spalla)")
    j3 = serializers.FloatField(help_text="Angolo Vincolo 3 (Gomito)")
    j4 = serializers.FloatField(help_text="Angolo Vincolo 4 (Pitch Polso)")
    j5 = serializers.FloatField(help_text="Angolo Vincolo 5 (Yaw Polso)")
    j6 = serializers.FloatField(help_text="Angolo Vincolo 6 (Roll Polso / Effettore Finale)")


class ConnectRequestSerializer(serializers.Serializer):
    """
    Serializer per la gestione della richiesta di inizio comunicazione (Handshake).
    """
    baudrate = serializers.IntegerField(
        default=115200, 
        required=False, 
        help_text="Velocità della porta seriale/bus I2C/SPI"
    )
    reset_to_home = serializers.BooleanField(
        default=False, 
        required=False, 
        help_text="Se True, forza l'homing di azzeramento al momento della connessione"
    )