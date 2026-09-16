# Definizione di metodo che permette di comandare il servo usando angoli in 365esimi.

from new.raspberry.FTServo_Python.scservo_sdk import COMM_SUCCESS

JOINTS = {
    1: {
        "zero_raw": 2510,
        "min_angle": -90,
        "max_angle": 90,
    },

    2: {
        "zero_raw": 1500,
        "min_angle": -45,
        "max_angle": 120,
    },

    3: {
        "zero_raw": 2320,
        "min_angle": -90,
        "max_angle": 90,
    },

    4: {
            "zero_raw": 35,
            "min_angle": -90,
            "max_angle": 90,
            "forbidden_raw": (1050, 3090)
    },

    5: {
            "zero_raw": 170,
            "min_angle": -180,
            "max_angle": 180,
    },

    6: {
            "zero_raw": 1080,
            "min_angle": 0,
            "max_angle": 90,
    },
}

def angle_to_raw(scs_id, angle_deg, steps_per_rev=4096):
    """
    angle_deg: angolo desiderato, es. -90, 0, +90 (0 = centro meccanico)
    center_raw: posizione raw corrispondente a angolo 0 (dipende da come hai
                fatto reOfsCal / dove è fisicamente montato il corno del servo)
    steps_per_rev: 4096 step = 360° per SMS/STS
    """
    joints = JOINTS[scs_id]
    zero_raw = joints["zero_raw"]
    raw = zero_raw + int(angle_deg * steps_per_rev / 360)
    return raw


def move_to_angle(packetHandler, scs_id, angle_deg, speed, acc):
    joints = JOINTS[scs_id]
    # clamp di sicurezza software, prima ancora di mandare il pacchetto
    angle_deg = max(joints["min_angle"], min(joints["max_angle"], angle_deg))

    pos = angle_to_raw(scs_id, angle_deg)
    forbidden_raw = joints.get("forbidden_raw")
    if forbidden_raw is not None:
        forbidden_min, forbidden_max = forbidden_raw
        if scs_id == 4 and forbidden_min < pos < forbidden_max:
            if (pos - forbidden_min) > (forbidden_max - pos):
                pos = forbidden_min
            else:
                pos = forbidden_max

    speed = abs(speed)  # forza sempre positivi
    acc = abs(acc)

    scs_comm_result, scs_error = packetHandler.WritePosEx(scs_id, pos, speed, acc)
    if scs_comm_result != COMM_SUCCESS:
        print(packetHandler.getTxRxResult(scs_comm_result))
    elif scs_error != 0:
        print(packetHandler.getRxPacketError(scs_error))
    return scs_comm_result, scs_error