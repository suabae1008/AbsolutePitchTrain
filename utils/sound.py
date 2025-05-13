# utils/sound.py
import threading
import time
from utils.serial_utils import send_period
from utils.constants import black_notes, white_notes
import pygame

def play_note_by_mode(note, is_black, sound_mode, ser, freq_map, exp_group,
                      white_sounds, black_sounds, pressed_keys=None, key=None):
    idx = (black_notes if is_black else white_notes).index(note)
    snd = black_sounds[idx] if is_black else white_sounds[idx]
    key_note = note[:-1]

    if sound_mode == 1:
        snd.play(-1)
        send_period(ser, freq_map, key_note, exp_group)

    elif sound_mode == 2:
        snd.play(-1)
        send_period(ser, freq_map, key_note, exp_group)

        def stop_after_1s():
            time.sleep(1.5)

            '''
            if key in pressed_keys and not pressed_keys[key].get("canceled", False):
                pressed_keys[key]["sound"].stop()
                if ser:
                    send_period(ser, freq_map, '0', exp_group)
            '''

            if key in pressed_keys and not pressed_keys[key].get("canceled", False):
                print(f"[DEBUG] ✅ Performing stop for key '{key}' – 1.5s elapsed without cancellation.")
                pressed_keys[key]["sound"].stop()
                if ser:
                    send_period(ser, freq_map, '0', exp_group)

            elif key in pressed_keys and pressed_keys[key].get("canceled", False):
                print(f"[DEBUG] ⚠️ Key '{key}' was canceled before timer expired. Skipping stop.")

            else:
                print(f"[DEBUG] ⛔ Key '{key}' was already removed before timer expired.")

        threading.Thread(target=stop_after_1s, daemon=True).start()


    elif sound_mode == 3:
        def fixed_play():
            snd.play()
            send_period(ser, freq_map, key_note, exp_group)
            time.sleep(1)
            snd.stop()
            send_period(ser, freq_map, '0', exp_group)
        threading.Thread(target=fixed_play).start()
