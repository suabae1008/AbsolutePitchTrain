import pygame
import time
import os
from pygame import mixer

from utils.constants import white_notes, black_notes, key_map, freq_map
from utils.draw import draw_piano
from utils.serial_utils import init_serial, send_period
from utils.sound import play_note_by_mode

'''
def run_instruction_training(sound_mode, exp_group):
    ser = init_serial(exp_group)

    pygame.init()
    mixer.init()
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
            # draw_piano(screen, font, white_notes, black_notes, label="Instruction Mode")
            # text_surface = font.render(inst['text'], True, (0, 0, 0))
            # screen.blit(text_surface, (20, 450))
            # pygame.display.flip()

            screen.fill('white')
            instruction_text = font.render(inst['text'], True, (0, 0, 0))
            mode_text = font.render("Instruction Mode (키보드에 출력된 피아노를 보고 입력하세요)", True, (0, 0, 0))
            screen.blit(mode_text, (40, 40))
            screen.blit(instruction_text, (40, 100))
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

    # draw_piano(screen, font, white_notes, black_notes, label="🎉 완료되었습니다!")
    screen.fill('white')
    done_msg = font.render("🎉 완료되었습니다! 수고하셨습니다.", True, (0, 0, 0))
    screen.blit(done_msg, (WIDTH // 2 - 180, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
'''

def run_instruction_training(sound_mode, ser=None):
    """
    sound_mode: 1, 2, 3
    ser: serial object (group 1일 때만 전달)
    """
    exp_group = 1 if ser else 0  # ser 존재 여부로 그룹 판단

    pygame.init()
    mixer.init()
    mixer.set_num_channels(64)

    white_sounds = [mixer.Sound(f'assets/notes/{n}.wav') for n in white_notes]
    black_sounds = [mixer.Sound(f'assets/notes/{n}.wav') for n in black_notes]

    WIDTH, HEIGHT = 1000, 600
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Instruction-Based Training")

    font_path = os.path.join("assets", "fonts", "Pretendard-Regular.ttf")
    font = pygame.font.Font(font_path, 20)

    instruction_list = [
        {
            "text": "1) 도부터 시까지 하얀 건반을 천천히 한 음씩 눌러보며 자극을 기억해보세요.",
            "notes_required": ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4'],
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

    pressed_keys = {}  # ✅ 자극 관리용
    clock = pygame.time.Clock()
    for inst in instruction_list:
        pressed_notes = set()
        start_time = time.time()
        running = True

        while running:
            screen.fill('white')
            
            # 안내 문구 (상단)
            mode_text = font.render("[지침 훈련] 화면의 안내에 따라 건반을 눌러보세요", True, (0, 0, 0))
            mode_rect = mode_text.get_rect(midtop=(WIDTH // 2, 60))
            screen.blit(mode_text, mode_rect)

            # 지시 문장 (본문)
            instruction_text = font.render(inst['text'], True, (0, 0, 0))
            instruction_rect = instruction_text.get_rect(midtop=(WIDTH // 2, 120))
            screen.blit(instruction_text, instruction_rect)
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

                        idx = (black_notes if is_black else white_notes).index(note)
                        snd = black_sounds[idx] if is_black else white_sounds[idx]

                        if sound_mode in [1, 2]:
                            pressed_keys[key] = {
                                'idx': idx,
                                'is_black': is_black,
                                'canceled': False,
                                'stopped': False,
                                'sound': snd
                            }

                        play_note_by_mode(note, is_black, sound_mode, ser, freq_map, exp_group,
                                          white_sounds, black_sounds, pressed_keys, key)

                elif event.type == pygame.KEYUP:
                    key = pygame.key.name(event.key).lower()
                    if key in pressed_keys:
                        info = pressed_keys[key]
                        info["canceled"] = True

                        if not info.get('stopped', False):
                            info['sound'].stop()
                            if ser:
                                send_period(ser, freq_map, '0', exp_group)
                            info['stopped'] = True

                        del pressed_keys[key]

            if inst['notes_required']:
                if set(inst['notes_required']).issubset(pressed_notes):
                    running = False
            elif inst['timeout']:
                if time.time() - start_time >= inst['timeout']:
                    running = False

            clock.tick(30)

    screen.fill('white')
    done_msg = font.render("🎉 완료되었습니다! 수고하셨습니다.", True, (0, 0, 0))
    screen.blit(done_msg, (WIDTH // 2 - 180, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
