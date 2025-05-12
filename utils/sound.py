# utils/sound.py
import threading
import time
from utils.serial_utils import send_period
from utils.constants import black_notes, white_notes
import pygame

def play_note_by_mode(note, is_black, sound_mode, ser, freq_map, exp_group,
                      white_sounds, black_sounds):
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
            time.sleep(1)
            if pygame.mixer.get_init():  # mixer가 살아있을 때만 stop 시도
                snd.stop()
                if ser:
                    send_period(ser, freq_map, '0', exp_group)

        threading.Thread(target=stop_after_1s, daemon=True).start()


    elif sound_mode == 3:
        def fixed_play():
            snd.play()
            send_period(ser, freq_map, key_note, exp_group)
            time.sleep(1)
            snd.stop()
            send_period(ser, freq_map, '0', exp_group)
        threading.Thread(target=fixed_play).start()
