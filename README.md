# **Titlu**  
**RoadDetect** – Sistem pentru detectarea obiectelor și streaming video live.

---

## **Scopul produsului**  
Crearea unui sistem compact și portabil pentru monitorizarea drumurilor, capabil să detecteze și să recunoască diverse obiecte (mașini, pietoni, semne rutiere) și să transmită în timp real fluxuri video.

---

## **Obiective**
1. **Detectare obiecte pe drum**: Mașini, pietoni, semne de circulație.
2. **Streaming video live**: Transmiterea imaginilor capturate de cameră pe un server web.
3. **Portabilitate**: Alimentare cu baterie Li-Ion, compatibilitate cu dispozitive compacte (Raspberry Pi Zero 2W).

---
## **Demo**
**Click For Video**

[![Demo Video](https://i.vimeocdn.com/video/1993758793-bd3f01c9706321f37ced4e42b1fab4e2ff70707435f2a20766bf6e8f5942ab2e-d_640x360?)](https://vimeo.com/1066114185)

[![Demo Video](https://i.vimeocdn.com/video/1993758777-dbb6d2a05d698e18368ba6e410819858c696fbe8adafd8131c123d0bf3bdbedf-d_640x360?)](https://vimeo.com/1066114141)

---

## **Hardware**
### **Modul de dezvoltare**
- **Raspberry Pi Zero 2W**: Procesor quad-core, dimensiune compactă, suport pentru Python și cameră dedicată.

### **Senzori și componente utilizate**
- **Cameră ultrawide pentru Raspberry Pi**:   
  - Rezoluție: 12MP  
  - Unghi: 120°
- **Baterie Li-Ion reîncărcabilă**:   
  - Capacitate: 20000mAh  
  - Tensiune: 5V usb/micro-usb

### **Diagrama de conectare**
- Raspberry Pi conectat la cameră ultrawide.
- Baterie conectată la Raspberry Pi printr-un cablu usb/micro-usb.

---

## **Software**
### **Verificare componente**
- Testare hardware utilizând comenzi de bază în Raspberry Pi (e.g., verificarea funcționării camerei cu `raspistill`).

### **Funcționalități implementate**
1. **Detectarea obiectelor** (`lane detection`):
   - Algoritm YOLO v8 pentru recunoaștere de obiecte.
   - Procesare video și salvare cu adnotări.
2. **Streaming video live** (`sender.py`):
   - Server Flask pentru transmiterea imaginilor capturate.
   - Configurare pentru accesarea fluxului video prin rețea locală.
3. **Detectare și salvare locala a imaginilor** ('reciever.py')
   - Algoritm YOLO v8 pentru recunoaștere de obiecte.
   - Procesare imaginilor in timp real și salvarea cu adnotări.

---

## **Instalare și configurare pe Raspberry Pi**
Pentru a utiliza scriptul **`sender.py`**, urmați pașii de mai jos pentru instalarea și configurarea Raspberry Pi Zero 2W. **Este obligatoriu să utilizați sistemul de operare `RASPBERRY PI OS LEGACY Bullseye`.**

### **Pași de instalare pentru partea streaming de pe Raspberry PI**
1. Instalați sistemul de operare **`RASPBERRY PI OS LEGACY Bullseye`** pe cardul SD utilizând unelte precum Raspberry Pi Imager.

2. Actualizați pachetele și sistemul:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. Configurați fișierul de setări:
   ```bash
   sudo nano /boot/config.txt
   ```
   - Suplimentați setările pentru camera modulului:  
     Adăugați următoarele linii dacă lipsesc:
     ```
     #-------RPi camera module-------
     start_x=1
     camera_auto_detect=1
     #-------GPU memory splits-------
     ```

4. Instalați componentele necesare:
   ```bash
   sudo apt install pip
   sudo apt install python3-picamera2
   sudo apt install libcamera-apps-lite
   sudo apt-get install ffmpeg
   ```

5. Verificați conexiunea camerei:
   ```bash
   libcamera-hello --list-cameras
   ```
   - Această comandă ar trebui să detecteze camera conectată.

### **Pași de instalare pentru partea clientului**
Pentru a utiliza scriptul de detectare cu YOLO v8, urmați pașii de mai jos:

1. **Crearea unui mediu virtual Conda**:
   ```bash
   conda create -n myenv python=3.8
   ```

2. **Activarea mediului virtual și instalarea dependențelor**:
   ```bash
   conda activate myenv
   pip install ultralyticsplus==0.0.23 ultralytics==8.0.21
   ```

3. **Rularea scriptului**:
   Executați scriptul folosind comanda:
   ```bash
   python reciever.py
   ```

Acest script va detecta obiectele în imaginea specificată și va afișa rezultatele vizual.

---



### **Pași de utilizare**
1. Asigurați-vă că toate conexiunile sunt corecte și componentele sunt bine instalate.
2. Rulați scriptul **`sender.py`** pentru a începe streaming-ul video:
   ```bash
   python3 sender.py
   ```

3. Odată pornit, dispozitivul va transmite fluxul video pe adresa **`udp://<IP>:9000`**.

4. După aceea, se poate rula scriptul **`reciever.py`** pentru a detecta in timp real obiecte

---

## **Depanare**
Dacă în timpul utilizării camera nu este detectată sau apar alte probleme, urmați pașii de mai jos:

1. Verificați fișierul de configurare al sistemului:
   ```bash
   sudo nano /boot/config.txt
   ```
   Asigurați-vă că liniile pentru camera modulului sunt corecte:
   ```
   #-------RPi camera module-------
   start_x=1
   camera_auto_detect=1
   #-------GPU memory splits-------
   ```

2. Reinstalați aplicațiile pentru cameră:
   ```bash
   sudo apt install libcamera-apps-lite
   ```

3. Testați camera utilizând comanda:
   ```bash
   libcamera-hello --list-cameras
   ```

4. Consultați sursa oficială de depanare, de exemplu:  [Adafruit Camera Troubleshooting](https://forums.adafruit.com/viewtopic.php?t=206375)

---

## **Bibliografie**

1. Documentația YOLO v8: [https://docs.ultralytics.com](https://docs.ultralytics.com)  
2. Ghid oficial Raspberry Pi: [https://www.raspberrypi.org](https://www.raspberrypi.org)  
3. Flask Documentation: [https://flask.palletsprojects.com](https://flask.palletsprojects.com)  
4. Adafruit Camera Troubleshooting: [https://forums.adafruit.com/viewtopic.php?t=206375](https://forums.adafruit.com/viewtopic.php?t=206375)  
5. Raspberry Pi Camera Guide: [https://raspberrytips.com/picamera2-raspberry-pi/](https://raspberrytips.com/picamera2-raspberry-pi/)  
6. Headless Raspberry Pi Setup: [https://electronicshacks.com/how-to-set-up-a-headless-raspberry-pi/#:~:text=Headless%20Raspberry%20Pi%20Setup%3A%201%201.%20Download%20the,remotely%20connected%20to%20your%20headless%20Raspberry%20Pi%21%20](https://electronicshacks.com/how-to-set-up-a-headless-raspberry-pi/#:~:text=Headless%20Raspberry%20Pi%20Setup%3A%201%201.%20Download%20the,remotely%20connected%20to%20your%20headless%20Raspberry%20Pi%21%20)  
7. Picamera2 Streaming with Python: [https://stackoverflow.com/questions/74131698/how-to-stream-a-capture-video-using-picamera2](https://stackoverflow.com/questions/74131698/how-to-stream-a-capture-video-using-picamera2)  
8. GStreamer Downloads: [https://gstreamer.freedesktop.org/download/#windows](https://gstreamer.freedesktop.org/download/#windows)


---

## **Date de contact**
Nume: [Radu George]  
E-mail: [george-i.radu@student.unitbv.ro]

