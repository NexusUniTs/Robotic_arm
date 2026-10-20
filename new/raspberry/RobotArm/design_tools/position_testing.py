import sys

sys.path.append("../../..")
from new.raspberry.RobotArm.FTServo_Python.scservo_sdk import *

# ============================================================
# CONFIGURAZIONE
# ============================================================

scs_id = 3
CONFIG_ADDR = 18
TORQUE_ENABLE_ADDR = SMS_STS_TORQUE_ENABLE

# ============================================================
# INIZIALIZZAZIONE
# ============================================================

portHandler = PortHandler('COM5')
packetHandler = sms_sts(portHandler)

if portHandler.openPort():
    print("Succeeded to open port")
else:
    print("Failed to open port")
    quit()

if portHandler.setBaudRate(1000000):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()


# ============================================================
# 1. LEGGI CONFIGURAZIONE ATTUALE
# ============================================================

config_before, result, error = packetHandler.read1ByteTxRx(
    scs_id,
    CONFIG_ADDR
)

if result != COMM_SUCCESS:
    print(packetHandler.getTxRxResult(result))
    quit()

print("\n===== PRIMA DELLA MODIFICA =====")
print("ID:", scs_id)
print("CONFIG:", config_before)
print("HEX:", hex(config_before))
print("BIT 4:", (config_before >> 4) & 1)


# ============================================================
# 2. LEGGI POSIZIONE ATTUALE
# ============================================================

pos_before, result, error = packetHandler.read2ByteTxRx(
    scs_id,
    SMS_STS_PRESENT_POSITION_L
)

if result != COMM_SUCCESS:
    print(packetHandler.getTxRxResult(result))
    quit()

pos_before = packetHandler.scs_tohost(pos_before, 15)

print("POSITION BEFORE:", pos_before)


# ============================================================
# 3. CALCOLA NUOVO VALORE
#    Cancella SOLO il BIT 4
# ============================================================

config_after = config_before & ~(1 << 4)

print("\n===== MODIFICA =====")
print("Vecchio valore:", config_before, hex(config_before))
print("Nuovo valore:  ", config_after, hex(config_after))

if config_after == config_before:
    print("Il bit 4 era già 0. Nessuna modifica necessaria.")
    quit()


# ============================================================
# 5. SBLOCCA EEPROM
# ============================================================

print("Sblocco EEPROM...")

result, error = packetHandler.unLockEprom(scs_id)

if result != COMM_SUCCESS:
    print(packetHandler.getTxRxResult(result))
    quit()


# ============================================================
# 6. SCRIVI IL NUOVO VALORE DEL REGISTRO 18
# ============================================================

print("Scrivo configurazione...")

result, error = packetHandler.write1ByteTxRx(
    scs_id,
    CONFIG_ADDR,
    config_after
)

if result != COMM_SUCCESS:
    print(packetHandler.getTxRxResult(result))
    quit()

if error != 0:
    print(packetHandler.getRxPacketError(error))
    quit()


# ============================================================
# 7. RIBLOCCA EEPROM
# ============================================================

print("Blocco EEPROM...")

result, error = packetHandler.LockEprom(scs_id)

if result != COMM_SUCCESS:
    print(packetHandler.getTxRxResult(result))
    quit()



# ============================================================
# 9. VERIFICA REGISTRO 18
# ============================================================

config_check, result, error = packetHandler.read1ByteTxRx(
    scs_id,
    CONFIG_ADDR
)

if result != COMM_SUCCESS:
    print(packetHandler.getTxRxResult(result))
    quit()

print("\n===== DOPO LA MODIFICA =====")
print("CONFIG:", config_check)
print("HEX:", hex(config_check))
print("BIT 4:", (config_check >> 4) & 1)


# ============================================================
# 10. VERIFICA POSIZIONE
# ============================================================

pos_after, result, error = packetHandler.read2ByteTxRx(
    scs_id,
    SMS_STS_PRESENT_POSITION_L
)

if result != COMM_SUCCESS:
    print(packetHandler.getTxRxResult(result))
    quit()

pos_after = packetHandler.scs_tohost(pos_after, 15)

print("POSITION AFTER:", pos_after)


# ============================================================
# RISULTATO FINALE
# ============================================================

print("\n========================================")
print("VERIFICA FINALE")
print("========================================")
print("Configurazione:", hex(config_before), "->", hex(config_check))
print("Bit 4:", (config_before >> 4) & 1, "->", (config_check >> 4) & 1)
print("Posizione:", pos_before, "->", pos_after)

if config_check == config_after and ((config_check >> 4) & 1) == 0:
    print("\nSUCCESSO: il bit 4 è stato disattivato.")
else:
    print("\nATTENZIONE: la configurazione non corrisponde a quella prevista.")