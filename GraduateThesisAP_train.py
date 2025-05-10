import pygame
from pygame import mixer
import time
import serial
import threading
import numpy

# 사용자 모드 입력
exp_group = int(input("CHOOSE MODE (CTRL-0 ETACTILE-1): "))
exp_group = float(exp_group)

sound_mode = int(input("SOUND MODE (1=hold, 2=hold_max_1s, 3=fixed_1s): "))


# 시리얼 포트 연결
if exp_group == 1:
    ser = serial.Serial('COM9', 9600, timeout=7)
    print("serial connected")
    ser.close()
    ser.open()

# 기본 세팅 ------------------------------------------------------------------------------
# 음계 정의
white_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4',
               'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5']
black_notes = ['Db4', 'Eb4', 'Gb4', 'Ab4', 'Bb4',
               'Db5', 'Eb5', 'Gb5', 'Ab5', 'Bb5']

# 음계-주파수 매핑
freq_map = {
    'C':95, 'Db':55, 'D':40, 'Eb':25, 'E':15,
    'F':8, 'Gb':4, 'G':8, 'Ab':15, 'A':25, 'Bb':40, 'B':55
}


# 실제 피아노 건반 순서 기준 키 매핑
key_map = {
    'tab': 'C4', '1': 'Db4', 'q': 'D4', '2': 'Eb4', 'w': 'E4',
    'e': 'F4', '4': 'Gb4', 'r': 'G4', '5': 'Ab4', 't': 'A4',
    '6': 'Bb4', 'y': 'B4', 'u': 'C5', '8': 'Db5', 'i': 'D5',
    '9': 'Eb5', 'o': 'E5', 'p': 'F5', '-': 'Gb5', '[': 'G5',
    '=': 'Ab5', ']': 'A5', '\\': 'Bb5', 'backspace': 'B5'
}



# 강조 상태
active_whites, active_blacks = [], []

# pygame 초기화
pygame.init()
mixer.set_num_channels(64)
white_sounds = [mixer.Sound(f'assets\\notes\\{n}.wav') for n in white_notes]
black_sounds = [mixer.Sound(f'assets\\notes\\{n}.wav') for n in black_notes]
WIDTH, HEIGHT = len(white_notes) * 40, 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("C4–B5 Piano Training")
font = pygame.font.SysFont(None, 48)


# 자극 전송 함수
def send_period(key_note):
    if exp_group == 1:
        channel_period = int(1000 / freq_map[key_note] + exp_group * 1000)
        ser.write((str(channel_period) + '\n').encode())
    

# 고정 1초 재생
def play_note_fixed(note, is_black, idx):
    snd = black_sounds[idx] if is_black else white_sounds[idx]
    snd.play()
    key_note = note[:-1]
    
    if exp_group == 1:
        send_period(int(1000 / freq_map[key_note] + exp_group * 1000))
        
    time.sleep(1)
    snd.stop()
    if exp_group == 1:
        send_period(0)
    (active_blacks if is_black else active_whites).remove(idx)


# 그리기 함수
def draw_piano():
    screen.fill('white')
    for i, note in enumerate(white_notes):
        c = 'lightblue' if i in active_whites else 'white'
        pygame.draw.rect(screen, c, [i * 40, 100, 40, 300])
        pygame.draw.rect(screen, 'black', [i * 40, 100, 40, 300], 2)
    black_idx = 0
    for i in range(len(white_notes) - 1):
        if white_notes[i][0] in ['E', 'B']: continue
        c = 'lightblue' if black_idx in active_blacks else 'black'
        pygame.draw.rect(screen, c, [i * 40 + 28, 100, 24, 180])
        black_idx += 1
    label = font.render(f"Mode {sound_mode}: C4~B5 훈련", True, (0, 0, 0))
    screen.blit(label, (20, 20))

# 메인 루프 ---------------------------------------------------------------------------------------------
run = True
pressed_keys = {}

while run:
    draw_piano()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key).lower()
            if key in key_map and key not in pressed_keys:
                note = key_map[key]
                is_black = note in black_notes
                idx = (black_notes if is_black else white_notes).index(note)
                snd = black_sounds[idx] if is_black else white_sounds[idx]
                key_note = note[:-1] # 옥타브 숫자 제거

                # 🚨 1번 : 누르는 만큼
                if sound_mode == 1:

                    snd.play(-1)

                    if exp_group == 1:
                        send_period(key_note)

                    (active_blacks if is_black else active_whites).append(idx)
                    
                    pressed_keys[key] = {
                        'sound': snd, 'note': note,
                        'start_time': time.time(), 'idx': idx, 'is_black': is_black
                    }

                # 🚨 2번 : 맥스 1초, 보다 짧게는 누르는 만큼 
                elif sound_mode == 2:

                    snd.play(-1)

                    if exp_group == 1:
                        send_period(key_note)
                        
                    (active_blacks if is_black else active_whites).append(idx)
                    
                    pressed_keys[key] = {
                        'sound': snd, 'note': note,
                        'start_time': time.time(), 'idx': idx,
                        'is_black': is_black, 'stopped': False
                    }

                    # 🧠 백그라운드로 1초 후 자동 종료 쓰레드 실행
                    def stop_after_1s(k=key):
                        time.sleep(1)
                        if k in pressed_keys and not pressed_keys[k]['stopped']:
                            pressed_keys[k]['sound'].stop()
                            if exp_group == 1:
                                send_period(0)
                            idx_ = pressed_keys[k]['idx']
                            if pressed_keys[k]['is_black']:
                                if idx_ in active_blacks: active_blacks.remove(idx_)
                            else:
                                if idx_ in active_whites: active_whites.remove(idx_)
                            pressed_keys[k]['stopped'] = True
                            del pressed_keys[k]

                    threading.Thread(target=stop_after_1s).start()

                # 🚨 3번 : 1초간 고정 
                elif sound_mode == 3:

                    (active_blacks if is_black else active_whites).append(idx)
                    threading.Thread(target=play_note_fixed, args=(note, is_black, idx)).start()

        elif event.type == pygame.KEYUP:
            key = pygame.key.name(event.key).lower()
            if key in pressed_keys:
                info = pressed_keys[key]

                # 이미 1초 스레드에서 처리한 경우: 아무것도 하지 않음
                if not info.get('stopped', False):
                    info['sound'].stop()
                    if exp_group == 1:
                        send_period(0)
                    idx = info['idx']
                    if info['is_black']:
                        if idx in active_blacks:
                            active_blacks.remove(idx)
                    else:
                        if idx in active_whites:
                            active_whites.remove(idx)
                    info['stopped'] = True  # 중복 방지
                del pressed_keys[key]


pygame.quit()
