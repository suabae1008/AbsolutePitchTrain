import pygame
from pygame import mixer
import time
import os

from utils.constants import white_notes, black_notes, key_map, freq_map
from utils.serial_utils import init_serial, send_period
from utils.draw import draw_piano
from utils.sound import play_note_by_mode

def run_piano_training(training_time, sound_mode, exp_group):
    ser = init_serial(exp_group)

    pygame.init()
    mixer.set_num_channels(64)

    white_sounds = [mixer.Sound(f'assets/notes/{n}.wav') for n in white_notes]
    black_sounds = [mixer.Sound(f'assets/notes/{n}.wav') for n in black_notes]

    WIDTH, HEIGHT = len(white_notes) * 40, 600
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("C4–B5 Piano Training")
    font_path = os.path.join("assets", "fonts", "Pretendard-Regular.ttf")
    font = pygame.font.Font(font_path, 20)

    active_whites, active_blacks = [], []
    pressed_keys = {}

    start_time = time.time()
    while time.time() - start_time < training_time:
        draw_piano(screen, font, white_notes, black_notes, active_whites, active_blacks,
                   label=f"Mode {sound_mode} 자유롭게 건반을 눌러보며, 자극을 느껴보세요")
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

                    (active_blacks if is_black else active_whites).append(idx)

                    # 모드별 재생 및 자극 전달
                    play_note_by_mode(note, is_black, sound_mode, ser, freq_map, exp_group,
                                      white_sounds, black_sounds)

                    # 누르고 있는 키 상태 저장 (모드 1, 2에서 떼야 멈춤)
                    if sound_mode in [1, 2]:
                        pressed_keys[key] = {
                            'idx': idx,
                            'is_black': is_black,
                            'stopped': False,
                            'sound': black_sounds[idx] if is_black else white_sounds[idx]
                        }

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
