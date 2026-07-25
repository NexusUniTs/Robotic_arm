import time
import requests
import random

SERVER_URL = "http://127.0.0.1:8000/api/pi_sync/"

def simulate_pi():
    current_joints = {'j1': 0.0, 'j2': 0.0, 'j3': 0.0, 'j4': 0.0, 'j5': 0.0, 'j6': 0.0}
    
    print("=========================================")
    print("Starting NEXUS Raspberry Pi Simulator")
    print("Waiting for dashboard sync...")
    print("=========================================\n")
    
    while True:
        try:
            # Simulate slight sensor noise
            voltage = 24.0 + random.uniform(-0.2, 0.2)
            temperature = 35.0 + random.uniform(-0.5, 0.5)
            # Simulate torque load relative to joints
            torque = sum(abs(v) for v in current_joints.values()) / 360 * 2.0
            
            payload = {
                'joints': current_joints,
                'status': {
                    'voltage': round(voltage, 1),
                    'temperature': round(temperature, 1),
                    'torque': round(torque, 2)
                }
            }
            
            response = requests.post(SERVER_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                target_joints = data.get('target_joints', current_joints)
                gripper_state = data.get('gripper', False)
                
                # Move joints towards targets gradually to simulate physical movement
                # Simulates the motors spinning up towards target angle
                for j in current_joints:
                    diff = float(target_joints[j]) - float(current_joints[j])
                    if abs(diff) > 2:
                        current_joints[j] += diff * 0.2 # move 20% of the way each iteration
                    else:
                        current_joints[j] = float(target_joints[j])
                
                # Pretty print status to console
                gripper_status_str = "ENGAGED" if gripper_state else "DISENGAGED"
                print(f"[SYNC OK] Torq: {payload['status']['torque']}Nm | Gripper: {gripper_status_str} | Targets: {target_joints}")
                print(f"          Current Joint True State: {current_joints}")
            else:
                print(f"Error {response.status_code} syncing with server.")
        
        except Exception as e:
            print(f"Connection failed (is the Django server running?): {e}")
            
        # Hardware polling rate
        time.sleep(1)

if __name__ == "__main__":
    simulate_pi()
