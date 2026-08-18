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

for scs_id in [1, 2]:

    pos, speed, comm_result, error = packetHandler.ReadPosSpeed(scs_id)

    if comm_result == COMM_SUCCESS:
        print(
            f"[ID:{scs_id}] "
            f"position={pos}, speed={speed}"
        )
    else:
        print(packetHandler.getTxRxResult(comm_result))