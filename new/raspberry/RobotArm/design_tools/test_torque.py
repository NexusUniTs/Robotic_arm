import sys

sys.path.append("../../..")
from new.raspberry.RobotArm.FTServo_Python.scservo_sdk import *

scs_id = 4

portHandler = PortHandler('COM5')
packetHandler = sms_sts(portHandler)

portHandler.openPort()
portHandler.setBaudRate(1000000)

result, error = packetHandler.write1ByteTxRx(
    scs_id,
    SMS_STS_TORQUE_ENABLE,
    0
)

if result == COMM_SUCCESS:
    print("Torque ID 4 DISABILITATO")
else:
    print(packetHandler.getTxRxResult(result))