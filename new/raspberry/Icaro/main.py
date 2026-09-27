from new.raspberry.Icaro.joint_conversion import raw_to_angle, angle_to_raw
from new.raspberry.Icaro.kinematics import solve_ik
from new.raspberry.Icaro.robot_arm import RobotArm
import numpy as np


def main():
    icaro = RobotArm()
    icaro.connect()

    q_raw = icaro.get_position()
    q_deg = []

    for i in range(5):
        q_deg.append(raw_to_angle(i+1, q_raw[i]))

    q_current = np.deg2rad(q_deg)

    x = 0.1
    y = 0.2
    z = 0.1
    q_solution = solve_ik(x, y, z, q_current)

    q_sol_deg = np.rad2deg(q_solution)
    q_sol_raw = []

    for i in range(5):
        q_sol_raw.append(angle_to_raw(i+1, q_sol_deg[i]))

    gripper_position = 1080

    icaro.move_arm(q_sol_raw, gripper_position)

    #Modulo per la ricezione delle posizioni dal master
    while True:
        q_master = receive_positions()

        icaro.move_arm(
            q_master[:5],
            q_master[5]
        )
    #Modulo per l'invio delle posizioni al slave
    while True:
        q_master = dedalo.get_position()

        send_positions(q_master)

        time.sleep(0.02)

    icaro.disconnect()

if __name__ == "__main__":
    main()