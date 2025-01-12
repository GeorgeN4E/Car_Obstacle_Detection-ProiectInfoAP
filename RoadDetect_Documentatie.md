
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
  - Capacitate: 2300mAh
  - Tensiune: 3.7V

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

## **Bibliografie**
1. Documentația YOLO v8: [https://docs.ultralytics.com](https://docs.ultralytics.com)
2. Ghid oficial Raspberry Pi: [https://www.raspberrypi.org](https://www.raspberrypi.org)
3. Flask Documentation: [https://flask.palletsprojects.com](https://flask.palletsprojects.com)

---

## **Date de contact**
Nume: [Numele tău]  
E-mail: [adresa ta de e-mail]  
Telefon: [numărul tău de telefon]  
