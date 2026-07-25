# Dashboard NEXUS - Braccio Robotico
Questa applicazione web, sviluppata in Django per il backend e HTML/Tailwind/JavaScript nativi per il frontend, ti permette di inviare comandi e ricevere dati in tempo reale da un nodo hardware simulato, che in questo caso fa le veci di un Raspberry Pi.

---

## Come avviare il progetto

Poiché l'applicazione web e il braccio robotico sono due componenti separati che comunicano tra loro, avrai bisogno di aprire due finestre del terminale per poter avviare sia il server web che il robot vero e proprio.

Entrambi i terminali dovranno essere aperti all'interno della cartella principale del progetto, ovvero `Nexus_Robo_Arm`.

### 1. Avviare il server web (Terminale 1)
Questa è la finestra del terminale che gestirà l'interfaccia utente.

- Apri un terminale nella cartella `Nexus_Robo_Arm`.
- Attiva l'ambiente virtuale Python digitando:
  ```bash
  source venv/bin/activate
  ```
- Fai partire il server web col comando:
  ```bash
  python manage.py runserver 8000
  ```

A questo punto l'interfaccia è pronta. Ti basta aprire il browser e visitare l'indirizzo [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### 2. Avviare il robot simulato (Terminale 2)
Se avvii solo il server web, la dashboard funzionerà ma sarà "ferma": non riceverà alcun dato né invierà comandi. Lo script di simulazione (`pi_simulator.py`) è il vero motore dietro le quinte: si occupa di scambiare in tempo reale l'angolazione dei motori e le letture di voltaggio con l'app web.

- Apri un nuovo terminale, sempre nella cartella `Nexus_Robo_Arm`.
- Attiva nuovamente l'ambiente virtuale:
  ```bash
  source venv/bin/activate
  ```
- Avvia lo script che simula il braccio del robot eseguendo:
  ```bash
  python pi_simulator.py
  ```

Fatto questo, il sistema è connesso. Inizierai a vedere dei messaggi sul terminale che ti confermano l'invio continuo dei dati alla dashboard.
Se provi ad andare sulla pagina web e modifichi, ad esempio, i gradi dell'asse "J1", vedrai i motori muoversi gradualmente sul terminale del robot, mentre sulla dashboard si aggiornerà in tempo reale il voltaggio del sistema.

---

## Come spegnere tutto

Quando hai finito, per fermare il sistema ti basterà interrompere l'esecuzione nei due terminali che avevi aperto.

1. **Torna al Terminale 1 (quello del server web)**
   - Clicca sulla finestra per attivarla.
   - Premi **`CTRL + C`** sulla tastiera. Il server web si arresterà immediatamente.

2. **Torna al Terminale 2 (quello del robot)**
   - Passa all'altra finestra del terminale.
   - Premi di nuovo **`CTRL + C`** sulla tastiera per interrompere lo script Python.

Tutto qui. Hai spento correttamente il sistema e liberato le risorse del computer.
