"""
Interfaccia hardware del braccio robotico RobotArm.

Questo modulo gestisce la comunicazione tra il software e il robot fisico
tramite la libreria FTServo.

Responsabilità principali:
- apertura e chiusura della connessione seriale;
- lettura delle posizioni attuali dei servomotori;
- invio dei comandi di posizione ai cinque giunti del braccio;
- controllo del servomotore della pinza.

Questo modulo non si occupa dei calcoli cinematici o della pianificazione
delle traiettorie.
"""
import sys

sys.path.append("../../..")
from FTServo_Python.scservo_sdk import *
from new.raspberry.RobotArm import icaro_joint_conversion


class RobotArm:
    def __init__(self):
        #Caratteristiche del robot
        self.servo_ids = [1, 2, 3, 4, 5, 6]
        self.portHandler = None
        self.packetHandler = None

    def connect(self, x):
        #Apre la comunicazione col robot
        self.portHandler = PortHandler("COM" + str(x))
        self.packetHandler = sms_sts(self.portHandler)

        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            quit()

        if self.portHandler.setBaudRate(1000000):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            quit()

    def disconnect(self):
        if self.portHandler is not None:
            self.portHandler.closePort()

    def get_position(self):
        q_pos = []
        for id in self.servo_ids:
            pos, speed, comm_result, error = self.packetHandler.ReadPosSpeed(id)
            if comm_result == COMM_SUCCESS:
                q_pos.append(pos)
            else:
                print(self.packetHandler.getTxRxResult(comm_result))
        return q_pos

    def move_arm(self, q_target, gripper_position):
        # Comandi i cinque gradi di libertà del braccio
        for i in range (5):

            q_raw = icaro_joint_conversion.angle_to_raw(i+1, q_target[i])
            self.packetHandler.SyncWritePosEx(i + 1, q_raw, 60, 50)

        #Comanda l'end effector

        gripper_raw = icaro_joint_conversion.angle_to_raw(6, gripper_position)
        self.packetHandler.SyncWritePosEx(6, gripper_raw, 60, 50)

        self.packetHandler.groupSyncWrite.txPacket()  # invia tutto in un colpo solo
        self.packetHandler.groupSyncWrite.clearParam()

    def move_joint(self, scs_id, target):
        q_raw = icaro_joint_conversion.angle_to_raw(scs_id, target)
        self.packetHandler.SyncWritePosEx(scs_id, q_raw, -150, 80)

        self.packetHandler.groupSyncWrite.txPacket()  # invia tutto in un colpo solo
        self.packetHandler.groupSyncWrite.clearParam()
