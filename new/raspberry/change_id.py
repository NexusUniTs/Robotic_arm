#!/usr/bin/env python
#
# *********     Change Servo ID (SMS/STS) - da ID 1 a ID arbitrario      *********
#
# ATTENZIONE: collega SOLO il motore di cui vuoi cambiare l'ID (deve essere su ID 1).
import sys
import os
import time

sys.path.append("..")
from FTServo_Python.scservo_sdk import *         # Uses FTServo SDK library

portHandler = PortHandler('COM5')
packetHandler = sms_sts(portHandler)

OLD_ID = 1

# Apertura porta
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()

if portHandler.setBaudRate(1000000):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()

# Chiedi il nuovo ID
NEW_ID = int(input("Inserisci il nuovo ID (1-252): "))

if NEW_ID < 1 or NEW_ID > 252:
    print("ID non valido. Deve essere tra 1 e 252.")
    portHandler.closePort()
    quit()

# Conferma che il motore risponde al vecchio ID
scs_model_number, scs_comm_result, scs_error = packetHandler.ping(OLD_ID)
if scs_comm_result != COMM_SUCCESS:
    print("[ID:%03d] %s" % (OLD_ID, packetHandler.getTxRxResult(scs_comm_result)))
    portHandler.closePort()
    quit()
print("[ID:%03d] ping Succeeded. Model number : %d" % (OLD_ID, scs_model_number))

# 1. Sblocca la EPROM
scs_comm_result, scs_error = packetHandler.unLockEprom(OLD_ID)
if scs_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(scs_comm_result))
    portHandler.closePort()
    quit()

# 2. Scrivi il nuovo ID
scs_comm_result, scs_error = packetHandler.write1ByteTxRx(OLD_ID, SMS_STS_ID, NEW_ID)
if scs_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(scs_comm_result))
    portHandler.closePort()
    quit()
if scs_error != 0:
    print("%s" % packetHandler.getRxPacketError(scs_error))

# 3. Riblocca la EPROM con il NUOVO ID
scs_comm_result, scs_error = packetHandler.LockEprom(NEW_ID)
if scs_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(scs_comm_result))

# 4. Verifica
scs_model_number, scs_comm_result, scs_error = packetHandler.ping(NEW_ID)
if scs_comm_result != COMM_SUCCESS:
    print("[ID:%03d] %s" % (NEW_ID, packetHandler.getTxRxResult(scs_comm_result)))
else:
    print("[ID:%03d] Cambio ID riuscito! Model number : %d" % (NEW_ID, scs_model_number))

portHandler.closePort()