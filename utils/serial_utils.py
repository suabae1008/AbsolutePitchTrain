# serial_utils.py

import serial
import time

import serial
import time

def init_serial(exp_group):
    if exp_group == 1:
        try:
            ser = serial.Serial('COM5', 9600, timeout=7)
            ser.close()
            ser.open()
            time.sleep(2)  # 아두이노 리셋 대기
            
            if ser.is_open:
                print("✅ Serial connection established on COM5")
                return ser
            else:
                print("❌ Failed to open serial port COM5")
                return None
        except serial.SerialException as e:
            print(f"❌ Serial connection error: {e}")
            return None
    return None


def send_period(ser, freq_map, key_note, exp_group):
    if ser:
        try:
            period = int(1000 / freq_map[key_note] + exp_group * 1000) if key_note != '0' else exp_group * 1000
            ser.write((str(period) + '\n').encode())
            print(f"✅ Sent period {period} for note '{key_note}' to Arduino")
        except Exception as e:
            print(f"❌ Failed to send period for note '{key_note}': {e}")

