"""
serializers.py - Serializers DRF per il server di controllo centrale
"""

from rest_framework import serializers


class JointUpdateSerializer(serializers.Serializer):
    """
    Serializer per la modifica dei 6 vincoli/joint dell'oggetto virtuale.
    Tutti i vincoli sono opzionali (required=False) per consentire sia
    l'aggiornamento parziale che totale dei valori.
    
    JSON di esempio:
    {
        "j1": 45.0,
        "j2": -10.0,
        "j3": 90.0,
        "j4": 0.0,
        "j5": 15.0,
        "j6": 180.0
    }
    """
    j1 = serializers.FloatField(required=False, help_text="Valore vincolo 1")
    j2 = serializers.FloatField(required=False, help_text="Valore vincolo 2")
    j3 = serializers.FloatField(required=False, help_text="Valore vincolo 3")
    j4 = serializers.FloatField(required=False, help_text="Valore vincolo 4")
    j5 = serializers.FloatField(required=False, help_text="Valore vincolo 5")
    j6 = serializers.FloatField(required=False, help_text="Valore vincolo 6")


class DeviceAuthSerializer(serializers.Serializer):
    """
    Serializer per l'autenticazione dei dispositivi (Raspberry Pi o Client).
    
    JSON di esempio:
    {
        "device_id": "rpi_arm_node_01",
        "secret_key": "raspberry_pi_secret_key_2026"
    }
    """
    device_id = serializers.CharField(max_length=100, help_text="Identificatore del dispositivo")
    secret_key = serializers.CharField(max_length=255, help_text="Chiave segreta/token del dispositivo")