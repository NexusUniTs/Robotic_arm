"""
virtual_arm.py - Classe per la virtualizzazione dello stato del braccio robotico
"""

class VirtualArmState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VirtualArmState, cls).__new__(cls)
            cls._instance.joints = {
                "j1": 0.0,
                "j2": 0.0,
                "j3": 0.0,
                "j4": 0.0,
                "j5": 0.0,
                "j6": 0.0,
            }
            cls._instance.status = "idle"
            cls._instance.last_updated_by = None
        return cls._instance

    def get_state(self) -> dict:
        """Restituisce lo stato attuale dell'oggetto virtuale."""
        return {
            "joints": self.joints.copy(),
            "status": self.status,
            "last_updated_by": self.last_updated_by
        }

    def update_joints(self, new_joints: dict, device_id: str = "unknown") -> dict:
        """Aggiorna i valori dei vincoli/joint nell'oggetto virtuale."""
        for joint_key, value in new_joints.items():
            if joint_key in self.joints and value is not None:
                self.joints[joint_key] = float(value)
        self.status = "active"
        self.last_updated_by = device_id
        return self.get_state()