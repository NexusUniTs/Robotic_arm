# RobotArm – Teleoperazione Icaro/Dedalo

Software di controllo per due bracci robotici a servomotori **Feetech STS/SMS** (protocollo SCS, libreria FTServo):

- **Dedalo**: braccio *leader*, mosso a mano dall'operatore. Se ne leggono le posizioni dei giunti.
- **Icaro**: braccio *follower*, che riproduce in tempo reale i movimenti di Dedalo.

Ogni braccio ha **5 gradi di libertà** più una **pinza** (6 servomotori con ID da 1 a 6). Il progetto include anche il modello cinematico (Denavit-Hartenberg) del manipolatore e una serie di script di utilità per configurare e collaudare i servomotori.

## Indice

- [Come funziona](#come-funziona)
- [Struttura del progetto](#struttura-del-progetto)
- [Requisiti](#requisiti)
- [Configurazione hardware](#configurazione-hardware)
- [Calibrazione dei giunti](#calibrazione-dei-giunti)
- [Utilizzo](#utilizzo)
- [Modello cinematico](#modello-cinematico)
- [Script di utilità e collaudo](#script-di-utilità-e-collaudo)
- [Note di sicurezza](#note-di-sicurezza)
- [Problemi noti e possibili miglioramenti](#problemi-noti-e-possibili-miglioramenti)

## Come funziona

Il flusso di teleoperazione è il seguente:

```
Dedalo (leader)                                        Icaro (follower)
  servo 1..6  ──► get_position() ──► raw_to_angle() ──► angle_to_raw() ──► move_arm() ──► servo 1..6
  (posizioni raw)                    (dedalo_joint_      (icaro_joint_
                                      conversion)         conversion)
```

1. Si leggono le posizioni raw (0–4095, 4096 step = 360°) dei sei servo di Dedalo.
2. Si convertono in angoli in gradi usando la calibrazione di Dedalo (zero fisico, verso di rotazione).
3. Gli angoli vengono riconvertiti in posizioni raw usando la calibrazione di Icaro, con validazione di limiti articolari e intervalli raw vietati.
4. I comandi di posizione vengono inviati ai servo di Icaro.

Poiché i due bracci hanno zeri meccanici e versi di rotazione diversi, lo **stesso angolo** corrisponde a **posizioni raw diverse** sui due robot: è compito dei moduli `*_joint_conversion` gestire questa differenza.

## Struttura del progetto

Gli import del codice si riferiscono al pacchetto `new.raspberry.RobotArm`. Nella cartella principale si trovano i moduli di produzione; tutti gli script di test, utilità e modellazione sono in `design_tools/`.

```
new/raspberry/RobotArm/
├── FTServo_Python/            # SDK Feetech (scservo_sdk), non incluso in questo repository
├── main.py                    # Teleoperazione completa: Dedalo -> Icaro (move_arm)
├── robot_arm.py               # Interfaccia hardware (porta seriale, lettura/scrittura servo)
├── dedalo_joint_conversion.py # Calibrazione e conversione angoli <-> raw di Dedalo
├── icaro_joint_conversion.py  # Calibrazione e conversione angoli <-> raw di Icaro
├── icaro_kinematics.py        # Modello DH, cinematica diretta e inversa
│
└── design_tools/              # Strumenti di sviluppo, collaudo e configurazione
    ├── main_test.py               # Teleoperazione giunto per giunto (move_joint)
    ├── move_to_angle.py           # Comando di un singolo servo in gradi, con clamp di sicurezza
    ├── robot_model.py             # Esempio interattivo: modello, IK, grafici e traiettoria
    ├── matrix_test.py             # Cinematica diretta con sole matrici NumPy
    ├── change_id.py               # Cambio ID di un servo
    ├── get_position.py            # Lettura posizione/velocità di un servo
    ├── angle_limit_setting.py     # Scrittura dei limiti angolari in EEPROM
    ├── position_testing.py        # Modifica del bit 4 del registro di configurazione 18
    ├── test_torque.py             # Disabilitazione della coppia
    ├── servo_test.py              # Ping e movimento di un servo (raw)
    ├── servo_angle_test.py        # Movimento di un servo in gradi
    ├── multi_servo_test.py        # Movimento sequenziale di più servo (raw)
    └── multi_servo_angle_test.py  # Movimento dei sei servo in gradi
```

### Moduli principali

| Modulo | Responsabilità |
|---|---|
| `robot_arm.py` | Classe `RobotArm`: apertura/chiusura della porta seriale, lettura delle posizioni (`get_position`), comando dei cinque giunti e della pinza (`move_arm`), comando di un singolo giunto (`move_joint`). Non esegue calcoli cinematici. |
| `icaro_joint_conversion.py` | Parametri di calibrazione di Icaro e funzioni `angle_to_raw`, `raw_to_angle`, `validate_angle`, `validate_raw`. |
| `dedalo_joint_conversion.py` | Come sopra, per Dedalo. I valori devono essere mantenuti allineati al robot fisico. |
| `icaro_kinematics.py` | Modello DH a 5 giunti, `solve_fk(q)` e `solve_ik(x, y, z, q0)`. Gli angoli sono in **radianti**. La pinza non fa parte del modello. |

## Requisiti

- Python 3.9 o superiore
- Libreria **FTServo_Python** (`scservo_sdk`) fornita da Feetech
- Dipendenze Python:

```bash
pip install numpy pyserial spatialmath-python roboticstoolbox-python
```

- Adattatore USB–seriale per bus servo (ad esempio la scheda URT di Feetech) per ciascun braccio

## Configurazione hardware

- Baudrate: **1 000 000**.
- Gli ID dei servo devono essere **univoci** su ciascun bus (1–6). Per assegnarli usare `change_id.py`.
- Le porte seriali sono indicate nel codice come `COMx` (Windows). In `main.py` Icaro è su `COM3` e Dedalo su `COM5`:

```python
icaro = RobotArm()
icaro.connect(3)    # apre "COM3"
dedalo = RobotArm()
dedalo.connect(5)   # apre "COM5"
```

Su Linux/macOS occorre modificare `RobotArm.connect()` (e gli script di utilità) per usare percorsi come `/dev/ttyUSB0`.

## Calibrazione dei giunti

I parametri sono nel dizionario `JOINTS` di ciascun modulo `*_joint_conversion.py`. Per ogni giunto:

| Campo | Significato |
|---|---|
| `zero_raw` | Posizione raw che corrisponde all'angolo 0° del modello |
| `direction` | Verso di rotazione (`+1` oppure `-1`) rispetto al modello |
| `min_angle`, `max_angle` | Limiti articolari in gradi |
| `forbidden_raw` | (opzionale) Intervallo raw vietato `(min, max)`, per zone di fine corsa meccanica |

La conversione utilizzata è:

```
raw   = zero_raw + direction * int(angolo_deg * 4096 / 360)
angolo = (raw - zero_raw) * direction * 360 / 4096
```

`angle_to_raw` valida l'angolo (`validate_angle`) e la posizione raw ottenuta (`validate_raw`), sollevando `ValueError` se un valore è fuori dai limiti.

Per ricalibrare un braccio:

1. Portare il giunto nella posizione di zero e leggerne il valore raw con `get_position.py`.
2. Riportare il valore in `zero_raw`.
3. Verificare il verso di rotazione e correggere `direction` se necessario.
4. Individuare i limiti meccanici e impostare `min_angle`/`max_angle` ed eventuale `forbidden_raw`.
5. Se serve un limite hardware, scriverlo nella EEPROM del servo con `angle_limit_setting.py`.

## Utilizzo

Gli script usano `sys.path.append("../../..")` e import assoluti del tipo `new.raspberry...`: vanno eseguiti in modo che il pacchetto `new` sia raggiungibile (ad esempio dalla cartella dello script, oppure con `PYTHONPATH` impostato sulla radice del progetto).

### Teleoperazione completa

```bash
python main.py
```

Lo script legge ciclicamente le posizioni di Dedalo, le converte e comanda Icaro tramite `move_arm()`. Il ciclo si interrompe con `Ctrl+C`; nel blocco `finally` entrambe le porte seriali vengono chiuse.

> `main.py` contiene, commentato, un esempio di uso della cinematica inversa per portare Icaro in una posizione cartesiana (x, y, z). Per usare Icaro in modo autonomo basta decommentarlo e rimuovere il ciclo di teleoperazione.

### Teleoperazione giunto per giunto

```bash
python design_tools/main_test.py
```

Variante che comanda i giunti uno alla volta con `move_joint()` e stampa gli angoli letti. Utile per il debug di un singolo giunto.

### Uso della classe `RobotArm` da codice

```python
from new.raspberry.RobotArm.robot_arm import RobotArm

arm = RobotArm()
arm.connect(3)                       # COM3

raw = arm.get_position()             # lista di 6 posizioni raw
arm.move_arm([0, 0, -90, 0, 0], 45)  # 5 angoli del braccio + pinza, in gradi
arm.move_joint(1, 30)                # singolo giunto, angolo in gradi

arm.disconnect()
```

## Modello cinematico

Il manipolatore a 5 DOF è modellato con la convenzione Denavit-Hartenberg (distanze in **metri**) tramite `roboticstoolbox`:

| Giunto | d [m] | a [m] | alpha [rad] | offset [rad] |
|---|---|---|---|---|
| 1 | 0.023 | 0 | π/2 | 0 |
| 2 | 0 | 0.152 | 0 | π/2 |
| 3 | 0 | 0.155 | 0 | 0 |
| 4 | 0 | 0 | −π/2 | −π/2 |
| 5 | 0.065 | 0 | 0 | 0 |

```python
import numpy as np
from new.raspberry.RobotArm.icaro_kinematics import solve_fk, solve_ik

T = solve_fk(np.zeros(5))                    # cinematica diretta -> SE3
q = solve_ik(0.1, 0.2, 0.1, q0=np.zeros(5))  # cinematica inversa (solo posizione XYZ)
```

La cinematica inversa usa `ikine_LM` con `mask=[1, 1, 1, 0, 0, 0]`: viene vincolata la sola **posizione**, l'orientamento dell'end-effector è libero. Se non converge viene sollevato `ValueError`.

- `design_tools/robot_model.py` mostra il modello completo: tabella DH, cinematica diretta, IK, verifica della soluzione, traiettoria `jtraj` a 100 campioni e animazione.
- `design_tools/matrix_test.py` calcola la cinematica diretta con sole matrici NumPy (nota: qui le lunghezze sono in **millimetri**).

## Script di utilità e collaudo

| Script | Funzione |
|---|---|
| `change_id.py` | Cambia l'ID di un servo (da ID 1 a un nuovo ID). **Collegare un solo motore alla volta.** |
| `get_position.py` | Legge posizione e velocità raw di un servo. |
| `angle_limit_setting.py` | Scrive in EEPROM i limiti angolari hardware (min/max) di un servo. |
| `position_testing.py` | Legge e modifica il bit 4 del registro di configurazione 18 (EEPROM) e confronta posizione e configurazione prima/dopo. |
| `test_torque.py` | Disabilita la coppia di un servo (ID 4), per muoverlo a mano. |
| `servo_test.py` | Ping e movimento di un servo con `WritePosEx`. |
| `servo_angle_test.py` | Movimento di un servo comandato in gradi con `move_to_angle`. |
| `multi_servo_test.py` | Movimento sequenziale di più servo con posizioni raw. |
| `multi_servo_angle_test.py` | Movimento dei sei servo comandati in gradi. |
| `design_tools/move_to_angle.py` | Funzione `move_to_angle(packetHandler, scs_id, angle, speed, acc)` con clamp ai limiti e gestione dell'intervallo vietato del giunto 4. |

Tutti questi script si trovano in `design_tools/`. Prima di lanciarli controllare la porta `COMx` e l'ID del servo impostati nel file.

## Note di sicurezza

- Prima di avviare la teleoperazione verificare che le calibrazioni di Icaro e Dedalo corrispondano ai robot fisici: uno zero errato produce movimenti inattesi.
- Tenere libero lo spazio di lavoro di Icaro e avere sempre a portata di mano l'alimentazione per spegnerlo.
- Gli script che scrivono in EEPROM (`change_id.py`, `angle_limit_setting.py`, `position_testing.py`) modificano in modo permanente la configurazione del servo: controllare ID e valori prima dell'esecuzione.
- I limiti `min_angle`/`max_angle` e `forbidden_raw` proteggono dai fine corsa meccanici: non allargarli senza aver verificato fisicamente la corsa del giunto.

## Problemi noti e possibili miglioramenti

Osservazioni emerse leggendo il codice:

- **Parametri duplicati**: `design_tools/move_to_angle.py` contiene una copia del dizionario `JOINTS` di Icaro con limiti diversi (±90°, ±180°) rispetto a `icaro_joint_conversion.py` (±270°, ±360°). Conviene avere un'unica fonte di verità, importando `icaro_joint_conversion`.
- **Letture incomplete**: se la lettura di un servo fallisce, `RobotArm.get_position()` restituisce una lista più corta di 6 elementi e `main.py` andrebbe in `IndexError`. Meglio restituire `None` per il giunto mancante o sollevare un'eccezione.
- **Velocità negativa in `move_joint`**: `move_joint` passa `-150` come velocità a `SyncWritePosEx`, mentre `move_to_angle` forza velocità e accelerazione positive. Verificare che il valore negativo sia effettivamente voluto.
- **Gestione del wrap-around**: `dedalo_joint_conversion.raw_to_angle` contiene correzioni specifiche per i giunti 3 e 4 (valori forzati a −179° / 90°) con condizioni parzialmente ridondanti; in `icaro_joint_conversion.angle_to_raw` ci sono clamp analoghi per i giunti 4 e 6. Sarebbe più robusto gestire il wrap con una funzione generica basata su `forbidden_raw`.
- **Intervallo vietato di Dedalo (giunto 3)**: `forbidden_raw = (91, 2160)` ha come estremo superiore lo stesso valore di `zero_raw`; controllare che sia quello voluto.
- **Frequenza del ciclo**: `main.py` usa `time.sleep(1)` (1 Hz), mentre `main_test.py` usa 10 ms. Per un inseguimento fluido è opportuno un periodo più breve, tenendo conto della durata delle letture seriali.
- **Portabilità**: le porte `COMx` sono scritte nel codice; sarebbe utile spostarle in un file di configurazione o in argomenti da riga di comando.
- **Limiti di `ikine_LM`**: il solutore viene inizializzato dalla configurazione corrente `q0`, ma la soluzione non è controllata rispetto ai limiti articolari prima dell'invio al robot (lo fa solo `angle_to_raw`).
- **Documentazione del codice**: i docstring di `angle_to_raw`/`raw_to_angle` fanno riferimento a parametri (`center_raw`) che non esistono più e vanno aggiornati.
