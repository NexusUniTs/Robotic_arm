"""
Modello cinematico del braccio robotico RobotArm.

Questo modulo contiene la modellizzazione del manipolatore a 5 gradi
di libertà secondo la convenzione di Denavit-Hartenberg.

Responsabilità principali:
- definizione del modello DH del robot;
- calcolo della cinematica diretta (FK);
- calcolo della cinematica inversa (IK);
- eventuali altri calcoli cinematici, come il Jacobiano.

Le coordinate articolari utilizzate dal modello cinematico sono espresse
in radianti.

Il servomotore della pinza non fa parte del modello cinematico.
"""
import numpy as np
from spatialmath import SE3
from roboticstoolbox import RevoluteDH, DHRobot

robot = DHRobot(
    [
        RevoluteDH(d= 0.023, alpha= np.pi/2),
        RevoluteDH(a=0.152, offset = np.pi/2),
        RevoluteDH(a = 0.155),
        RevoluteDH(alpha= -np.pi/2, offset = -np.pi/2),
        RevoluteDH(d = 0.065)
    ], name='RobotArm'
)

def solve_fk(q):
    return robot.fkine(q)

def solve_ik(x, y, z, q0):
    T_target = SE3(x, y, z)
    solution = robot.ikine_LM(T_target, q0, mask=[1, 1, 1, 0, 0, 0])

    if not solution.success:
        raise ValueError("Inverse kinematics failed")

    return solution.q