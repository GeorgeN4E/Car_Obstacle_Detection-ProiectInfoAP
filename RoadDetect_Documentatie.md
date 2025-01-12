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
- Baterie conectată la Raspberry Pi printr-un modul de încărcare (TP4056).

---

## **Software**
### **Verificare componente**
- Testare hardware utilizând comenzi de bază în Raspberry Pi (e.g., verificarea funcționării camerei cu `raspistill`).

### **Funcționalități implementate**
1. **Detectarea obiectelor** (`road_detection.py`):
   - Algoritm YOLO v8 pentru recunoaștere de obiecte.
   - Procesare video și salvare cu adnotări.
2. **Streaming video live** (`stream.py`):
   - Server Flask pentru transmiterea imaginilor capturate.
   - Configurare pentru accesarea fluxului video prin rețea locală.

---

## **Instalare și configurare pe Raspberry Pi**
Pentru a utiliza scriptul **`sender.py`**, urmați pașii de mai jos pentru instalarea și configurarea Raspberry Pi Zero 2W. **Este obligatoriu să utilizați sistemul de operare `RASPBERRY PI OS LEGACY Bullseye`.**

### **Pași de instalare**
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

### **Pași de utilizare**
1. Asigurați-vă că toate conexiunile sunt corecte și componentele sunt bine instalate.
2. Rulați scriptul **`sender.py`** pentru a începe streaming-ul video:
   ```bash
   python3 sender.py
   ```

3. Odată pornit, dispozitivul va transmite fluxul video pe adresa **`udp://<IP>:9000`**.

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

---

## **Date de contact**
Nume: [Numele tău]  
E-mail: [adresa ta de e-mail]  
Telefon: [numărul tău de telefon]

