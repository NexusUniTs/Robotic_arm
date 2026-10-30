import time

from new.raspberry.RobotArm import icaro_joint_conversion, dedalo_joint_conversion
from new.raspberry.RobotArm.icaro_joint_conversion import raw_to_angle, angle_to_raw
from new.raspberry.RobotArm.icaro_kinematics import solve_ik
from new.raspberry.RobotArm.robot_arm import RobotArm
import numpy as np



icaro = RobotArm()
icaro.connect(3)
dedalo = RobotArm()
dedalo.connect(5)

try:
    while True:
        q_raw_dedalo = dedalo.get_position()

        q_dedalo = dedalo_joint_conversion.raw_to_angle(1, q_raw_dedalo[0])
        print(q_dedalo)
        icaro.move_joint(1, q_dedalo)

        q_dedalo=dedalo_joint_conversion.raw_to_angle(2, q_raw_dedalo[1])
        print(q_dedalo)
        icaro.move_joint(2, q_dedalo)

        q_dedalo = dedalo_joint_conversion.raw_to_angle(3, q_raw_dedalo[2])
        print(q_dedalo)
        icaro.move_joint(3, q_dedalo)

        q_dedalo = dedalo_joint_conversion.raw_to_angle(4, q_raw_dedalo[3])
        print(q_dedalo)
        icaro.move_joint(4, q_dedalo)

        q_dedalo = dedalo_joint_conversion.raw_to_angle(5, q_raw_dedalo[4])
        print(q_dedalo)
        icaro.move_joint(5, q_dedalo)

        q_dedalo = dedalo_joint_conversion.raw_to_angle(6, q_raw_dedalo[5])
        print(q_dedalo)
        icaro.move_joint(6, q_dedalo)




        '''

        icaro.move_arm(
            q_dedalo[:5],
            q_dedalo[5]
        )
        
        for i in range(6):
            print("ID " + str(i+1) + ": " + str(q_raw_dedalo[i]))
        '''
        time.sleep(0.01)
finally:
    icaro.disconnect()
    dedalo.disconnect()