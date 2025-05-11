# serial_utils.py

import serial

def init_serial(exp_group):
    if exp_group == 1:
        ser = serial.Serial('COM9', 9600, timeout=7)
        ser.close()
        ser.open()
        return ser
    return None

def send_period(ser, freq_map, key_note, exp_group):
    if ser:
        period = int(1000 / freq_map[key_note] + exp_group * 1000)
        ser.write((str(period) + '\n').encode())
