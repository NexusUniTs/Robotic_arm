import numpy as np
from spatialmath import SE3
import roboticstoolbox as rtb
from roboticstoolbox import RevoluteDH
from roboticstoolbox.robot import DHRobot

#Modellizzazione di RobotArm (manipolatore robotico a 5 gradi di libertà) secondo la convenzione DH
robot = DHRobot(
    [
        RevoluteDH(d= 0.023, alpha= np.pi/2),
        RevoluteDH(a=0.152, offset = np.pi/2),
        RevoluteDH(a = 0.155),
        RevoluteDH(alpha= -np.pi/2, offset = -np.pi/2),
        RevoluteDH(d = 0.065)
    ], name='RobotArm'
)
# Stampa il modello del robot e la relativa tabella DH
print(robot)

# Definisce una configurazione dei giunti e ne calcola la posa
# dell'end-effector tramite cinematica diretta

q_test=([np.pi/2, np.pi/2, np.pi/3, np.pi/2, 0])
T_test = robot.fkine(q_test)

print("Target:")
print(T_test)

robot.plot(q_test, block=True)

# Definisce la posa target dell'end-effector.
# In questo caso viene specificata solamente la posizione desiderata:
# x = 0.2 m, y = 0.1 m, z = 0.2 m.
T_target = SE3(0.2, 0.1, 0.2)

# Risolve numericamente la cinematica inversa partendo da q0.
# La mask impone solo la posizione XYZ e lascia libero
# l'orientamento dell'end-effector.
sol = robot.ikine_LM(T_target, q0=np.zeros(5), mask=[1, 1, 1, 0, 0, 0])

print(sol)
print("Angoli trovati: ", sol.q)

robot.plot(sol.q, block=True)
#Utilizzo la FK con i valori dei giunti trovati per ricalcolare la posizione consegnata alla IK
# e vedere se la rispetta.
T_solution = robot.fkine(sol.q)
print(T_solution)

# Genera una traiettoria nello spazio dei giunti composta da 100 campioni,
# dalla configurazione iniziale q0 alla configurazione trovata dalla IK.
traj = rtb.jtraj(np.zeros(5), sol.q, 100)
traj = rtb.jtraj(np.zeros(5), sol.q, 100,)
#Animiamo il movimento del braccio
robot.plot(traj.q, block=True)