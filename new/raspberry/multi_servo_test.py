import sys
import os
import time

sys.path.append("..")
from FTServo_Python.scservo_sdk import *                   # Uses FTServo SDK library


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler('COM5') #ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

# Initialize PacketHandler instance
# Get methods and members of Protocol
packetHandler = sms_sts(portHandler)
# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()

# Set port baudrate 1000000
if portHandler.setBaudRate(1000000):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()

motor_ids = [1, 2]

for scs_id in motor_ids:
    scs_model_number, scs_comm_result, scs_error = packetHandler.ping(scs_id)
    if scs_comm_result != COMM_SUCCESS:
        print("[ID:%03d] %s" % (scs_id, packetHandler.getTxRxResult(scs_comm_result)))
    else:
        print("[ID:%03d] ping Succeeded. Model number : %d" % (scs_id, scs_model_number))
    if scs_error != 0:
        print("[ID:%03d] %s" % (scs_id, packetHandler.getRxPacketError(scs_error)))

# Servo (ID1) runs at a maximum speed of V=400 * 0.732=43.92rpm and an acceleration of A=80 * 8.7deg/s ^ 2 until it reaches position P1=4095
scs_comm_result, scs_error = packetHandler.WritePosEx(1, 1000, 100, 60)
if scs_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(scs_comm_result))
elif scs_error != 0:
    print("%s" % packetHandler.getRxPacketError(scs_error))

time.sleep(3)

# Servo (ID2) runs at a maximum speed of V=60 * 0.732=43.92rpm and an acceleration of A=50 * 8.7deg/s ^ 2 until it reaches position P1=4095
scs_comm_result, scs_error = packetHandler.WritePosEx(2, 2000, 400, 80)
if scs_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(scs_comm_result))
elif scs_error != 0:
    print("%s" % packetHandler.getRxPacketError(scs_error))

time.sleep(((4095 - 0) / (60 * 50) + (60 * 50) / (50 * 100) + 0.05))  # [(P1-P0)/(V*50)] + [(V*50)/(A*100)] + 0.05

portHandler.closePort()