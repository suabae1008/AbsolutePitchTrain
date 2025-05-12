import pygame
import time
import os
from pygame import mixer

from utils.constants import white_notes, black_notes, key_map, freq_map
from utils.draw import draw_piano
from utils.serial_utils import init_serial, send_period
from utils.sound import play_note_by_mode

def run_instruction_training(sound_mode, exp_group):
    ser = init_serial(exp_group)

    pygame.init()
    mixer.set_num_channels(64)

    white_sounds = [mixer.Sound(f'assets/notes/{n}.wav') for n in white_notes]
    black_sounds = [mixer.Sound(f'assets/notes/{n}.wav') for n in black_notes]

    WIDTH, HEIGHT = len(white_notes) * 40, 600
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Instruction-Based Training")

    font_path = os.path.join("assets", "fonts", "Pretendard-Regular.ttf")
    font = pygame.font.Font(font_path, 20)

    instruction_list = [
    {
        "text": "1) 도부터 시까지 하얀 건반을 천천히 한 음씩 눌러보며 자극을 기억해보세요.",
        "notes_required": ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5'],
        "timeout": None
    },
    {
        "text": "2) 익숙하지 않은 검은 건반들도 눌러보며 자극을 비교해보세요.",
        "notes_required": ['Db4', 'Eb4', 'Gb4', 'Ab4', 'Bb4'],
        "timeout": None
    },
    {
        "text": "3) 도–미–솔을 순서대로 눌러보세요. (C4, E4, G4)",
        "notes_required": ['C4', 'E4', 'G4'],
        "timeout": None
    },
    {
        "text": "4) 레–파–라를 순서대로 눌러보세요. (D4, F4, A4)",
        "notes_required": ['D4', 'F4', 'A4'],
        "timeout": None
    },
    {
        "text": "5) 미–솔–시를 순서대로 눌러보세요. (E4, G4, B4)",
        "notes_required": ['E4', 'G4', 'B4'],
        "timeout": None
    },
    {
        "text": "6) 기억에 남는 자극이 있는 음을 다시 눌러보세요. (30초 자유 탐색)",
        "notes_required": None,
        "timeout": 30
    }
    ]   


    clock = pygame.time.Clock()
    for inst in instruction_list:
        pressed_notes = set()
        start_time = time.time()
        running = True

        while running:
            draw_piano(screen, font, white_notes, black_notes, label="Instruction Mode")
            text_surface = font.render(inst['text'], True, (0, 0, 0))
            screen.blit(text_surface, (20, 450))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key).lower()
                    if key in key_map:
                        note = key_map[key]
                        pressed_notes.add(note)
                        is_black = note in black_notes

                        play_note_by_mode(note, is_black, sound_mode, ser, freq_map, exp_group,
                                          white_sounds, black_sounds)

                elif event.type == pygame.KEYUP:
                    key = pygame.key.name(event.key).lower()
                    if key in key_map:
                        note = key_map[key]
                        is_black = note in black_notes
                        idx = (black_notes if is_black else white_notes).index(note)
                        snd = black_sounds[idx] if is_black else white_sounds[idx]
                        snd.stop()
                        send_period(ser, freq_map, '0', exp_group)

            # 종료 조건
            if inst['notes_required']:
                if set(inst['notes_required']).issubset(pressed_notes):
                    running = False
            elif inst['timeout']:
                if time.time() - start_time >= inst['timeout']:
                    running = False

            clock.tick(30)

    draw_piano(screen, font, white_notes, black_notes, label="🎉 완료되었습니다!")
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
