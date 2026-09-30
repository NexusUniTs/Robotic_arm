"""
Configurazione e conversione delle coordinate articolari di RobotArm.

Questo modulo contiene i parametri di calibrazione dei singoli giunti
e gestisce la conversione tra gli angoli del modello del robot e le
posizioni raw utilizzate dai servomotori.

Responsabilità principali:
- memorizzazione degli zero fisici dei giunti;
- definizione dei versi di rotazione;
- definizione dei limiti articolari;
- gestione di eventuali intervalli raw vietati;
- conversione da angoli in gradi a posizioni raw;
- conversione da posizioni raw ad angoli in gradi;
- validazione dei comandi prima dell'invio ai servomotori.

Questo modulo costituisce il collegamento tra il modello matematico
del robot e il sistema di coordinate dei servomotori fisici.
"""

JOINTS = {
    1: {
        "zero_raw": 2510,
        "min_angle": -90,
        "max_angle": 90,
        "direction": 1,
    },

    2: {
        "zero_raw": 2450,
        "min_angle": -90,
        "max_angle": 90,
        "direction": -1,
    },

    3: {
        "zero_raw": 200,
        "min_angle": -180,
        "max_angle": 0,
        "direction": -1,
    },

    4: {
            "zero_raw": 3180,
            "min_angle": -90,
            "max_angle": 90,
            "forbidden_raw": (64, 2060),
            "direction": -1,
    },

    5: {
            "zero_raw": 3190,
            "min_angle": -180,
            "max_angle": 180,
            "direction": 1,
    },

    6: {
            "zero_raw": 1080,
            "min_angle": 0,
            "max_angle": 90,
            "direction": 1,

    },
}

def validate_angle(scs_id, angle_deg):
    joints = JOINTS[scs_id]

    if not joints["min_angle"] <= angle_deg <= joints["max_angle"]:
        raise ValueError(
            f"Joint {scs_id}: angle {angle_deg}° out of range"
        )

def validate_raw(scs_id, raw):
    joints = JOINTS[scs_id]
    forbidden_raw = joints.get("forbidden_raw")

    if forbidden_raw is not None:
        forbidden_min, forbidden_max = forbidden_raw
        if forbidden_min < raw < forbidden_max:
            raise ValueError(
                f"Joint {scs_id}: raw position {raw} "
                f"is inside forbidden range {forbidden_raw}"
            )


def angle_to_raw(scs_id, angle_deg, steps_per_rev=4096):
    """
    angle_deg: angolo desiderato, es. -90, 0, +90 (0 = centro meccanico)
    center_raw: posizione raw corrispondente a angolo 0 (dipende da come hai
                fatto reOfsCal / dove è fisicamente montato il corno del servo)
    steps_per_rev: 4096 step = 360° per SMS/STS
    """
    validate_angle(scs_id, angle_deg)
    joints = JOINTS[scs_id]
    zero_raw = joints["zero_raw"]
    direction = joints["direction"]
    raw = zero_raw + direction*int(angle_deg * steps_per_rev / 360)
    validate_raw(scs_id, raw)
    return raw

def raw_to_angle(scs_id, angle_raw, steps_per_rev=4096):
    """
    angle_raw: angolo desiderato in 4096esimi
    center_raw: posizione raw corrispondente a angolo 0 (dipende da come hai
                fatto reOfsCal / dove è fisicamente montato il corno del servo)
    steps_per_rev: 360 step
    """
    joints = JOINTS[scs_id]
    zero_raw = joints["zero_raw"]
    direction = joints["direction"]
    angle_deg = (angle_raw - zero_raw)*direction*360/steps_per_rev

    return angle_deg