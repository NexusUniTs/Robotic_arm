# Questo codice si occupa di riscrivere i limiti meccanici di rotazione di un servo specificato
# con il scs_id, impostando MAX_ANGLE e MIN_ANGLE sulla memoria EPROM
import sys

sys.path.append("../../..")
from new.raspberry.Icaro.FTServo_Python.scservo_sdk import *

scs_id = 5
min_pos = 0
max_pos = 4095

portHandler = PortHandler('COM3')
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


# 1. Sblocca la EPROM
scs_comm_result, scs_error = packetHandler.unLockEprom(scs_id)
if scs_comm_result != COMM_SUCCESS:
    print(packetHandler.getTxRxResult(scs_comm_result))

# 2. Scrivi il limite minimo
scs_comm_result, scs_error = packetHandler.write2ByteTxRx(scs_id, SMS_STS_MIN_ANGLE_LIMIT_L, min_pos)
if scs_comm_result != COMM_SUCCESS:
    print(packetHandler.getTxRxResult(scs_comm_result))
elif scs_error != 0:
    print(packetHandler.getRxPacketError(scs_error))

# 3. Scrivi il limite massimo
scs_comm_result, scs_error = packetHandler.write2ByteTxRx(scs_id, SMS_STS_MAX_ANGLE_LIMIT_L, max_pos)
if scs_comm_result != COMM_SUCCESS:
    print(packetHandler.getTxRxResult(scs_comm_result))
elif scs_error != 0:
    print(packetHandler.getRxPacketError(scs_error))

# 4. Riblocca la EPROM
scs_comm_result, scs_error = packetHandler.LockEprom(scs_id)
if scs_comm_result != COMM_SUCCESS:
    print(packetHandler.getTxRxResult(scs_comm_result))