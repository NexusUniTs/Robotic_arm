import numpy as np
from spatialmath import SE3
import roboticstoolbox as rtb
from roboticstoolbox import RevoluteDH
from roboticstoolbox.robot import DHRobot

robot = DHRobot(
    [
        RevoluteDH(d= 0.023, alpha= np.pi/2),
        RevoluteDH(a=0.152, offset = np.pi/2),
        RevoluteDH(a = 0.155),
        RevoluteDH(alpha= -np.pi/2, offset = -np.pi/2),
        RevoluteDH(d = 0.065)
    ], name='NexusArm'
)

print(robot)
'''
q=np.zeros(5)
q_test=([0, np.pi/6, np.pi/3, np.pi/2, np.pi/18])
T_target = robot.fkine(q_test)

print("Target:")
print(T_target)

sol = robot.ikine_LM(T_target, q0=np.zeros(5), mask=[1, 1, 1, 0, 0, 0])

print(sol)
print(sol.q)

T_solution = robot.fkine(sol.q)

print("Target position:")
print(T_target.t)

print("IK position:")
print(T_solution.t)

print("Errore:")
print(T_target.t - T_solution.t)
'''
q = np.array([
    0,
    np.pi/6,
    np.pi/3,
    np.pi/2,
    np.pi/18
])

J = robot.jacob0(q)

print(J)
print("Rank:", np.linalg.matrix_rank(J))