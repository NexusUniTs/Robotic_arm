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
from FTServo_Python.scservo_sdk import *


class RobotArm:
    def __init__(self):
        #Caratteristiche del robot
        self.servo_ids = [1, 2, 3, 4, 5, 6]
        self.port_handler = None
        self.packet_handler = None

    def connect(self):
        #Apre la comunicazione col robot
        self.port_handler = PortHandler("COMx")
        self.packet_handler = sms_sts(port_handler)

        if port_handler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            quit()

        if port_handler.setBaudRate(1000000):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            quit()

    def disconnect(self):
        if self.port_handler is not None:
            self.port_handler.closePort()

    def get_position(self):
        q_pos = []
        for scs_id in self.servo_ids:
            pos, speed, comm_result, error = self.packet_handler.ReadPosSpeed(scs_id)
            if comm_result == COMM_SUCCESS:
                q_pos.append(pos)
            else:
                print(self.packet_handler.getTxRxResult(comm_result))
        return (q_pos)

    def move_arm(self, q_target, gripper_position):
        #Comandi i cinque gradi di libertà del braccio
        for i in range (5):
            self.packet_handler.SyncWritePosEx(i+1, q_target[i], 60, 50)
        #Comanda l'end effector
        self.packet_handler.SyncWritePosEx(6, gripper_position, 60, 50)

        self.packet_handler.groupSyncWrite.txPacket()  # invia tutto in un colpo solo
        self.packet_handler.groupSyncWrite.clearParam()