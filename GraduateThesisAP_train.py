import pygame
from pygame import mixer
import time
import serial
import threading


# 글로벌 변수 - 음계 정의 및 키보드 매핑

white_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4',
                'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5']
black_notes = ['Db4', 'Eb4', 'Gb4', 'Ab4', 'Bb4',
                'Db5', 'Eb5', 'Gb5', 'Ab5', 'Bb5']

key_map = {
    'tab': 'C4', '1': 'Db4', 'q': 'D4', '2': 'Eb4', 'w': 'E4',
    'e': 'F4', '4': 'Gb4', 'r': 'G4', '5': 'Ab4', 't': 'A4',
    '6': 'Bb4', 'y': 'B4', 'u': 'C5', '8': 'Db5', 'i': 'D5',
    '9': 'Eb5', 'o': 'E5', 'p': 'F5', '-': 'Gb5', '[': 'G5',
    '=': 'Ab5', ']': 'A5', '\\': 'Bb5', 'backspace': 'B5'
}


# 피아노 트레이닝 함수 정의
def run_piano_training(training_time, sound_mode, exp_group):
    
    # 실험군 - 아두이노 연결 
    if exp_group == 1:
        ser = serial.Serial('COM9', 9600, timeout=7)
        print("serial connected")
        ser.close()
        ser.open()

    else:
        ser = None

    # 음계 주파수 매핑
    freq_map = {
        'C':95, 'Db':55, 'D':40, 'Eb':25, 'E':15,
        'F':8, 'Gb':4, 'G':8, 'Ab':15, 'A':25, 'Bb':40, 'B':55
    }

    # 화이트/블랙 건반 음계에 해당하는 사운드 파일(.wav) 불러오기
    white_sounds = [mixer.Sound(f'assets\\notes\\{n}.wav') for n in white_notes]
    black_sounds = [mixer.Sound(f'assets\\notes\\{n}.wav') for n in black_notes]


    # pygame 모듈 초기화 및 화면 초기 세팅
    pygame.init()
    mixer.set_num_channels(64)
    WIDTH, HEIGHT = len(white_notes) * 40, 600
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("C4–B5 Piano Training")
    font = pygame.font.SysFont(None, 48)


    active_whites, active_blacks = [], [] # 눌린 키 인덱스 저장 리스트
    pressed_keys = {} # 눌린 키 정보 저장 딕셔너리

    # 아두이노 전송 함수 (*주기로 인코딩해 전달)
    def send_period(key_note):
        if ser:
            period = int(1000 / freq_map[key_note] + exp_group * 1000)
            ser.write((str(period) + '\n').encode())

    # 1초 플레이 고정
    def play_note_fixed(note, is_black, idx):
        snd = black_sounds[idx] if is_black else white_sounds[idx]
        snd.play()
        key_note = note[:-1]
        if ser:
            send_period(key_note)
        time.sleep(1)
        snd.stop()
        if ser:
            send_period(0)
        (active_blacks if is_black else active_whites).remove(idx)

    # 피아노 그리기 함수
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

    # 메인 루프 시작
    start_time = time.time()
    
    while time.time() - start_time < training_time:
        
        draw_piano()

        # 실제 화면에 그려진 내용을 갱신 (모니터에 표시)
        pygame.display.flip()

         # pygame이 감지한 사용자 이벤트(키보드 입력 등)를 하나씩 처리
        for event in pygame.event.get():

            # 창 닫기 버튼을 누르면 루프 종료
            if event.type == pygame.QUIT:
                return

            # 키보드를 눌렀을 때
            elif event.type == pygame.KEYDOWN:

                # 키 정보 수집
                key = pygame.key.name(event.key).lower()

                if key in key_map and key not in pressed_keys:
                    note = key_map[key]
                    is_black = note in black_notes
                    idx = (black_notes if is_black else white_notes).index(note)
                    snd = black_sounds[idx] if is_black else white_sounds[idx]
                    
                    # 옥타브 정보 제거 (D4>D)
                    key_note = note[:-1]

                    # [모드 1] 누르고 있는 동안 계속 소리 나기
                    if sound_mode == 1:
                        snd.play(-1)

                        if ser:
                            send_period(key_note)

                        (active_blacks if is_black else active_whites).append(idx)

                        # 키 상태 저장
                        pressed_keys[key] = {
                            'sound': snd, 'note': note,
                            'start_time': time.time(), 'idx': idx, 'is_black': is_black
                        }

                    # [모드 2] 최대 1초까지, 누른 만큼 재생
                    elif sound_mode == 2:
                        snd.play(-1)

                        if ser:
                            send_period(key_note)

                        (active_blacks if is_black else active_whites).append(idx)

                        pressed_keys[key] = {
                            'sound': snd, 'note': note,
                            'start_time': time.time(), 'idx': idx,
                            'is_black': is_black, 'stopped': False
                        }

                        # 백그라운드 쓰레드로 1초 후 강제 정지
                        def stop_after_1s(k=key):
                            time.sleep(1)

                            # 만약 사용자가 1초 안에 키를 떼지 않았다면 강제로 소리 정지
                            if k in pressed_keys and not pressed_keys[k]['stopped']:
                                
                                pressed_keys[k]['sound'].stop()

                                if ser:
                                    send_period(0)

                                idx_ = pressed_keys[k]['idx']

                                if pressed_keys[k]['is_black']:
                                    if idx_ in active_blacks: active_blacks.remove(idx_)
                                else:
                                    if idx_ in active_whites: active_whites.remove(idx_)
                                pressed_keys[k]['stopped'] = True

                                del pressed_keys[k]

                        threading.Thread(target=stop_after_1s).start()

                    # [모드 3] 무조건 1초 동안만 소리 나기
                    elif sound_mode == 3:

                        (active_blacks if is_black else active_whites).append(idx)
                        threading.Thread(target=play_note_fixed, args=(note, is_black, idx)).start()
            
            # 키보드 떼짐
            elif event.type == pygame.KEYUP:

                # 떼진 event key에 대해서 정보 가져옴
                key = pygame.key.name(event.key).lower()

                if key in pressed_keys:
                    info = pressed_keys[key]
                    
                    # stopped 필드 확인 후 
                    if not info.get('stopped', False):

                        info['sound'].stop()

                        if ser:
                            send_period(0)

                        idx = info['idx']

                        # 강조 해제
                        if info['is_black']:
                            if idx in active_blacks: active_blacks.remove(idx)
                        else:
                            if idx in active_whites: active_whites.remove(idx)

                        info['stopped'] = True
                    del pressed_keys[key]

    pygame.quit()
