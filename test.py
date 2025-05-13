import pygame
import random
import time
import pandas as pd
from pygame import mixer
from utils.constants import white_notes_test, black_notes_test, key_map, freq_map
from utils.serial_utils import send_period
import os
from openpyxl import load_workbook

def run_note_identification_test(num_questions, sub, mode, ser=None):
    """
    mode: 'test' or 'validation'
    - 'test': auditory only
    - 'validation': exp_group==1이면 auditory + tactile, exp_group==0이면 auditory only
    ser: serial object if stimulation is available (only for group 1)
    """

    give_stim = (mode == "validation" and ser is not None)

    pygame.init()
    mixer.init()
    mixer.set_num_channels(64)

    WIDTH, HEIGHT = 1000, 600
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Note Identification Test")
    font_path = os.path.join("assets", "fonts", "Pretendard-Regular.ttf")
    font = pygame.font.Font(font_path, 20)

    white_sounds = [mixer.Sound(f"assets/notes/{n}.wav") for n in white_notes_test]
    black_sounds = [mixer.Sound(f"assets/notes/{n}.wav") for n in black_notes_test]

    participant_answers = []
    correct_answers = []

    img_path = os.path.join("assets", "speaker.png")
    speaker_img = pygame.image.load(img_path)
    speaker_img = pygame.transform.scale(speaker_img, (200, 200))

    num_white = num_questions // 2
    num_black = num_questions - num_white
    selected_white = random.sample(white_notes_test, num_white)
    selected_black = random.sample(black_notes_test, num_black)
    target_notes = selected_white + selected_black
    random.shuffle(target_notes)

    # 시작 전 대기
    screen.fill('white')
    label = font.render("테스트를 시작하려면 ENTER 키를 눌러주세요", True, (0, 0, 0))
    label_rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(label, label_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

    idx = 0
    clock = pygame.time.Clock()
    run = True
    while run and idx < num_questions:
        screen.fill('white')
        # 텍스트 중앙 정렬
        label = font.render(f"Question {idx + 1} / {num_questions}", True, (0, 0, 0))
        label_rect = label.get_rect(midtop=(WIDTH // 2, 60))
        screen.blit(label, label_rect)

        # 이미지 중앙 정렬
        speaker_rect = speaker_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(speaker_img, speaker_rect)
        pygame.display.flip()
        clock.tick(30)

        current_note = target_notes[idx]
        snd = (
            white_sounds[white_notes_test.index(current_note)]
            if current_note in white_notes_test
            else black_sounds[black_notes_test.index(current_note)]
        )

        key_note = current_note[:-1]  # e.g., C4 → C

        snd.play()
        if give_stim:
            send_period(ser, freq_map, key_note, exp_group=1)

        time.sleep(1)  # 자극 및 소리 지속 시간

        if give_stim:
            send_period(ser, freq_map, '0', exp_group=1)

        # 응답 대기 (소리 끝나고 나서!)
        waiting_input = True
        input_start = time.time()
        while waiting_input and (time.time() - input_start) < 5:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    waiting_input = False
                elif event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key).lower()
                    if key in key_map:
                        guessed_note = key_map[key]
                        participant_answers.append(guessed_note[:-1])
                        correct_answers.append(current_note[:-1])
                        print(f"User answered: {guessed_note}")
                        waiting_input = False
                        idx += 1

        if waiting_input:
            participant_answers.append("-")
            correct_answers.append(current_note[:-1])
            print("No response within 5 seconds.")
            idx += 1

        time.sleep(3)

    # 결과 저장
    data = {
        "Correct": correct_answers,
        "Answer": participant_answers
    }
    df = pd.DataFrame(data)

    result_file = r"C:/Users/User/Desktop/SKKU/2025-1/졸업 논문 작성/result.xlsx"
    sheet_name = f"{mode}_{sub}"

    if not os.path.exists(result_file):
        with pd.ExcelWriter(result_file, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        with pd.ExcelWriter(result_file, engine="openpyxl", mode="a", if_sheet_exists="new") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"✅ Result saved to sheet '{sheet_name}' in {result_file}")
    pygame.quit()
