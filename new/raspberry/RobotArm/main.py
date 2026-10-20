import time

from new.raspberry.RobotArm import icaro_joint_conversion, dedalo_joint_conversion
from new.raspberry.RobotArm.icaro_joint_conversion import raw_to_angle, angle_to_raw
from new.raspberry.RobotArm.icaro_kinematics import solve_ik
from new.raspberry.RobotArm.robot_arm import RobotArm
import numpy as np


def main():
    #Se si vuole eseguire questo codice su Dedalo va modificato il main
    icaro = RobotArm()
    icaro.connect(3)
    dedalo = RobotArm()
    dedalo.connect(5)
    '''
    q_raw = icaro.get_position()
    q_deg = []

    for i in range(5):
        q_deg.append(icaro_joint_conversion.raw_to_angle(i+1, q_raw[i]))

    q_current = np.deg2rad(q_deg)

    x = 0.1
    y = 0.2
    z = 0.1
    q_solution = solve_ik(x, y, z, q_current)

    q_sol_deg = np.rad2deg(q_solution)
    q_sol_raw = []

    for i in range(5):
        q_sol_raw.append(icaro_joint_conversion.angle_to_raw(i+1, q_sol_deg[i]))

    gripper_position = 1080

    icaro.move_arm(q_sol_raw, gripper_position)
    '''
    #Modulo per la timezone delle position da Dedalo
    try:
        while True:
            q_raw_dedalo = dedalo.get_position()
            q_dedalo = []

            for i in range(6):
                q_dedalo.append(dedalo_joint_conversion.raw_to_angle(i + 1, q_raw_dedalo[i]))


            icaro.move_arm(
                q_dedalo[:5],
                q_dedalo[5]
            )
            '''
            for i in range(6):
                print("ID " + str(i+1) + ": " + str(q_raw_dedalo[i]))
            '''
            time.sleep(1)
    finally:
        icaro.disconnect()
        dedalo.disconnect()


if __name__ == "__main__":
    main()