
'''
import pygame
import random
import time
import pandas as pd
from pygame import mixer
from GraduateThesisAP_train import white_notes, black_notes, key_map  # 동일하게 사용할 리스트들


def run_note_identification_test(num_questions):
    # 초기화
    pygame.init()
    mixer.init()
    mixer.set_num_channels(64)

    WIDTH, HEIGHT = len(white_notes) * 40, 600
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Note Identification Test")
    font = pygame.font.SysFont(None, 48)

    white_sounds = [mixer.Sound(f"assets/notes/{n}.wav") for n in white_notes]
    black_sounds = [mixer.Sound(f"assets/notes/{n}.wav") for n in black_notes]

    active_whites, active_blacks = [], []
    participant_answers = []
    correct_answers = []

    # 무작위 정답 리스트 생성
    total_notes = white_notes + black_notes
    target_notes = random.choices(total_notes, k=num_questions)

    def draw_piano():
        screen.fill('white')
        for i, note in enumerate(white_notes):
            c = 'lightblue' if i in active_whites else 'white'
            pygame.draw.rect(screen, c, [i * 40, 100, 40, 300])
            pygame.draw.rect(screen, 'black', [i * 40, 100, 40, 300], 2)
        black_idx = 0
        for i in range(len(white_notes) - 1):
            if white_notes[i][0] in ['E', 'B']:
                continue
            c = 'lightblue' if black_idx in active_blacks else 'black'
            pygame.draw.rect(screen, c, [i * 40 + 28, 100, 24, 180])
            black_idx += 1
        label = font.render(f"Identify note {len(participant_answers)+1}/{num_questions}", True, (0, 0, 0))
        screen.blit(label, (20, 20))

    idx = 0
    clock = pygame.time.Clock()
    run = True
    while run and idx < num_questions:
        draw_piano()
        pygame.display.flip()
        clock.tick(30)

        # 정답 음 재생 (1회)
        current_note = target_notes[idx]
        if current_note in white_notes:
            snd = white_sounds[white_notes.index(current_note)]
        else:
            snd = black_sounds[black_notes.index(current_note)]
        snd.play()
        time.sleep(1)
        snd.stop()

        waiting_input = True
        while waiting_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    waiting_input = False
                elif event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key).lower()
                    if key in key_map:
                        guessed_note = key_map[key]
                        participant_answers.append(guessed_note)
                        correct_answers.append(current_note)

                        # 하이라이트
                        if guessed_note in white_notes:
                            idx_ = white_notes.index(guessed_note)
                            active_whites.append(idx_)
                        else:
                            idx_ = black_notes.index(guessed_note)
                            active_blacks.append(idx_)

                        waiting_input = False
                        idx += 1

    # 결과 저장
    data = {
        "Correct": correct_answers,
        "Answer": participant_answers
    }
    df = pd.DataFrame(data)
    filename = f"note_test_results_{int(time.time())}.xlsx"
    df.to_excel(filename, index=False)
    print(f"Result saved to {filename}")

    pygame.quit()
'''
#%%
import pygame
import random
import time
import pandas as pd
from pygame import mixer
from GraduateThesisAP_train import white_notes, black_notes, key_map
import os
from openpyxl import load_workbook



def run_note_identification_test(num_questions, sub):

    test_mode = input("TEST MODE (baseline/after/1day): ")
    # 초기화
    pygame.init()
    mixer.init()
    mixer.set_num_channels(64)

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Note Identification Test")
    font = pygame.font.SysFont(None, 48)

    white_sounds = [mixer.Sound(f"assets/notes/{n}.wav") for n in white_notes]
    black_sounds = [mixer.Sound(f"assets/notes/{n}.wav") for n in black_notes]

    participant_answers = []
    correct_answers = []

    # 이미지 로드 (스피커 이미지)
    img_path = os.path.join("assets", "speaker.png")  # 업로드된 이미지명에 맞게 수정
    speaker_img = pygame.image.load(img_path)
    speaker_img = pygame.transform.scale(speaker_img, (200, 200))

    # 무작위 정답 리스트 생성 (절반 흰 건반, 절반 검은 건반)
    num_white = num_questions // 2
    num_black = num_questions - num_white
    selected_white = random.sample(white_notes, num_white)
    selected_black = random.sample(black_notes, num_black)
    combined = selected_white + selected_black
    random.shuffle(combined)
    target_notes = combined

    # 시작 전 Enter 입력 대기
    waiting = True
    screen.fill('white')
    label = font.render("Press ENTER to start the test", True, (0, 0, 0))
    screen.blit(label, (WIDTH // 2 - 200, HEIGHT // 2))
    pygame.display.flip()
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

        # 정답 카운터 표시
        label = font.render(f"Question {idx + 1} / {num_questions}", True, (0, 0, 0))
        screen.blit(label, (WIDTH // 2 - 120, 50))

        # 이미지 표시
        screen.blit(speaker_img, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
        pygame.display.flip()
        clock.tick(30)

        # 정답 음 재생 (1회)
        current_note = target_notes[idx]
        if current_note in white_notes:
            snd = white_sounds[white_notes.index(current_note)]
        else:
            snd = black_sounds[black_notes.index(current_note)]
        snd.play()
        time.sleep(1)
        snd.stop()

        # 사용자 입력 대기 (최대 5초)
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
                        participant_answers.append(guessed_note)
                        correct_answers.append(current_note)
                        print(f"User answered: {guessed_note}")  # ✅ 디버그용 출력
                        waiting_input = False
                        idx += 1

        # 응답 없었으면 빈 응답 처리
        if waiting_input:
            participant_answers.append("-")
            correct_answers.append(current_note)
            print("No response within 5 seconds. Skipping.")  # ✅ 디버그용 출력
            idx += 1

        time.sleep(3)

    # 결과 저장
    data = {
        "Correct": correct_answers,
        "Answer": participant_answers
    }
    df = pd.DataFrame(data)

    # 🔄 기존 result.xlsx에 시트 추가 방식으로 저장
    result_file = r"C:/Users/User/Desktop/SKKU/2025-1/졸업 논문 작성/result.xlsx"  # 🔄 저장 경로 변경
    sheet_name = f"{test_mode}_{sub}"

    if not os.path.exists(result_file):
        # 파일이 없으면 새로 생성
        with pd.ExcelWriter(result_file, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        # 파일이 있으면 시트 추가
        with pd.ExcelWriter(result_file, engine="openpyxl", mode="a", if_sheet_exists="new") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Result saved to sheet '{sheet_name}' in {result_file}")

    pygame.quit()