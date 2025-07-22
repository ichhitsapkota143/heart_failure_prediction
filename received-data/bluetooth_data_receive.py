import serial
import time
import requests
import threading
from collections import deque

# === USER SETTINGS ===
PORT = "COM7"
BAUD = 9600
DJANGO_URL = "http://127.0.0.1:8000/bluetooth/get_bluetooth_data/"
MAXLEN = 300

# === INIT SERIAL ===
try:
    ser = serial.Serial(PORT, BAUD, timeout=0.1)
    print(f"Connected to {PORT} at {BAUD} baud.")
    time.sleep(2)
except Exception as e:
    print(f"Serial connection error: {e}")
    exit()

# === DATA BUFFERS ===
ecg_data = deque([0] * MAXLEN, maxlen=MAXLEN)
current_mode = None

# === Send to Django ===
def send_to_django(data_dict):
    try:
        response = requests.post(DJANGO_URL, json=data_dict, timeout=2)
        if response.status_code == 200:
            print("Sent to Django")
        else:
            print(f"Django error: Status code {response.status_code}")
    except Exception as e:
        print(f"Failed to send to Django: {e}")

# === Serial Reading Thread ===
def serial_reader():
    global current_mode
    while True:
        try:
            if ser.in_waiting > 0:
                raw_line = ser.readline()
                if not raw_line:
                    continue

                try:
                    line = raw_line.decode('utf-8', errors='ignore').strip()
                except UnicodeDecodeError:
                    continue  # Skip malformed lines

                if not line or len(line) < 3:
                    continue  # Ignore short or garbage lines

                print("Received:", line)

                # === Detect Mode Switch ===
                if "Switched to mode" in line:
                    if "ECG" in line:
                        current_mode = "ECG"
                        print("\nECG MODE ACTIVE")
                    elif "MAX30100" in line:
                        current_mode = "MAX30100"
                        print("\nMAX30100 MODE ACTIVE")
                    continue

                # === ECG Mode Handling ===
                if current_mode == "ECG" and line.startswith("ECG:"):
                    try:
                        val_str = line.split(":")[1].strip()
                        val = int(val_str)
                        ecg_data.append(val)
                        send_to_django({
                            "mode": "ECG",
                            "ecg_value": val
                        })
                    except Exception as e:
                        print("ECG parse error:", e)

                # === MAX30100 Handling ===
                elif current_mode == "MAX30100" and "SPO2" in line:
                    try:
                        parts = line.replace(" ", "").split(",")
                        data_dict = {
                            "mode": "MAX30100",
                            "spo2": float(parts[0].split(":")[1]),
                            "bpm": float(parts[1].split(":")[1]),
                            "glucose": float(parts[2].split(":")[1]),
                            "cholesterol": float(parts[3].split(":")[1])
                        }
                        send_to_django(data_dict)
                        print(f"MAX30100 DATA: {data_dict}")
                    except Exception as e:
                        print("MAX30100 parse error:", e)

        except Exception as e:
            print("Serial read loop error:", e)

        time.sleep(0.01)

# === Start Thread ===
serial_thread = threading.Thread(target=serial_reader, daemon=True)
serial_thread.start()

# === Main Program Loop ===
try:
    print("Starting data processing...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🔌 Exiting...")
finally:
    if ser:
        ser.close()
