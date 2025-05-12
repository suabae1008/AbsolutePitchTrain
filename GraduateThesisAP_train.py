import pygame
from pygame import mixer
import time
import threading
import os

from utils.constants import white_notes, black_notes, key_map, freq_map
from utils.serial_utils import init_serial, send_period
from utils.draw import draw_piano

def run_piano_training(training_time, sound_mode, exp_group):
    # 아두이노 설정
    ser = init_serial(exp_group)

    pygame.init()
    mixer.set_num_channels(64)

    # 사운드 로드
    white_sounds = [mixer.Sound(f'assets\\notes\\{n}.wav') for n in white_notes]
    black_sounds = [mixer.Sound(f'assets\\notes\\{n}.wav') for n in black_notes]

    # UI 초기화
    WIDTH, HEIGHT = len(white_notes) * 40, 600
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("C4–B5 Piano Training")
    font_path = os.path.join("assets", "fonts", "Pretendard-Regular.ttf")
    font = pygame.font.Font(font_path, 20)

    active_whites, active_blacks = [], []
    pressed_keys = {}

    def play_note_fixed(note, is_black, idx):
        snd = black_sounds[idx] if is_black else white_sounds[idx]
        snd.play()
        key_note = note[:-1]
        send_period(ser, freq_map, key_note, exp_group)
        time.sleep(1)
        snd.stop()
        send_period(ser, freq_map, '0', exp_group)
        (active_blacks if is_black else active_whites).remove(idx)

    start_time = time.time()
    while time.time() - start_time < training_time:
        draw_piano(screen, font, white_notes, black_notes, active_whites, active_blacks, label=f"Mode {sound_mode} 자유롭게 건반을 눌러보며, 자극을 느껴보세요")
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key).lower()
                if key in key_map and key not in pressed_keys:
                    note = key_map[key]
                    is_black = note in black_notes
                    idx = (black_notes if is_black else white_notes).index(note)
                    snd = black_sounds[idx] if is_black else white_sounds[idx]
                    key_note = note[:-1]

                    if sound_mode == 1:
                        snd.play(-1)
                        send_period(ser, freq_map, key_note, exp_group)
                        (active_blacks if is_black else active_whites).append(idx)
                        pressed_keys[key] = {
                            'sound': snd, 'note': note,
                            'start_time': time.time(), 'idx': idx, 'is_black': is_black
                        }

                    elif sound_mode == 2:
                        snd.play(-1)
                        send_period(ser, freq_map, key_note, exp_group)
                        (active_blacks if is_black else active_whites).append(idx)
                        pressed_keys[key] = {
                            'sound': snd, 'note': note,
                            'start_time': time.time(), 'idx': idx,
                            'is_black': is_black, 'stopped': False
                        }

                        def stop_after_1s(k=key):
                            time.sleep(1)
                            if k in pressed_keys and not pressed_keys[k]['stopped']:
                                pressed_keys[k]['sound'].stop()
                                send_period(ser, freq_map, '0', exp_group)
                                idx_ = pressed_keys[k]['idx']
                                if pressed_keys[k]['is_black']:
                                    if idx_ in active_blacks: active_blacks.remove(idx_)
                                else:
                                    if idx_ in active_whites: active_whites.remove(idx_)
                                pressed_keys[k]['stopped'] = True
                                del pressed_keys[k]

                        threading.Thread(target=stop_after_1s).start()

                    elif sound_mode == 3:
                        (active_blacks if is_black else active_whites).append(idx)
                        threading.Thread(target=play_note_fixed, args=(note, is_black, idx)).start()

            elif event.type == pygame.KEYUP:
                key = pygame.key.name(event.key).lower()
                if key in pressed_keys:
                    info = pressed_keys[key]
                    if not info.get('stopped', False):
                        info['sound'].stop()
                        send_period(ser, freq_map, '0', exp_group)
                        idx = info['idx']
                        if info['is_black']:
                            if idx in active_blacks: active_blacks.remove(idx)
                        else:
                            if idx in active_whites: active_whites.remove(idx)
                        info['stopped'] = True
                    del pressed_keys[key]

    pygame.quit()
