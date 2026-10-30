#!/usr/bin/env python

import os
import sys

# Importa lo SDK di Feetech / SCServo
from scservo_sdk import COMM_SUCCESS, PortHandler, sms_sts

# 1. Imposta la tua porta COM5 di Windows al posto di /dev/ttyUSB0
portHandler = PortHandler("COM5")

# 2. Inizializza l'interfaccia per la serie SMS/STS
packetHandler = sms_sts(portHandler)

# Apri la porta COM5
if portHandler.openPort():
    print("Porta COM5 aperta con successo!")
else:
    print("Errore nell'aprire la porta COM5.")
    sys.exit()

# Imposta il Baud Rate a 1.000.000 (1 Mbps, di default per gli STS)
if portHandler.setBaudRate(1000000):
    print("Baudrate impostato a 1000000 con successo!")
else:
    print("Errore nell'impostare il baudrate.")
    portHandler.closePort()
    sys.exit()

# Tenta un PING al servo con ID 1
SCS_ID = 1
scs_model_number, scs_comm_result, scs_error = packetHandler.ping(SCS_ID)

if scs_comm_result != COMM_SUCCESS:
    print(f"Errore comunicazione: {packetHandler.getTxRxResult(scs_comm_result)}")
else:
    print(f"[ID:{SCS_ID:03d}] Ping riuscito! Modello Servo: {scs_model_number}")

if scs_error != 0:
    print(f"Errore interno del servo: {packetHandler.getRxPacketError(scs_error)}")

# Chiudi la porta al termine
portHandler.closePort()
print("Porta chiusa.")
