# from GraduateThesisAP_test import run_note_identification_test
from test import run_note_identification_test
from GraduateThesisAP_train import run_piano_training
from GraduateThesisAP_instruction import run_instruction_training

def main():
    print("🎓 E-Tactile Absolute Pitch Training 시작")

    # 사용자 정보 입력
    '''
    sub = input("SUBJECT INITIAL: ")
    exp_group = int(input("CHOOSE MODE (CTRL-0, ETACTILE-1): "))
    sound_mode = int(input("SOUND MODE (1=hold, 2=hold_max_1s, 3=fixed_1s): "))
    '''

    sub = "BSA_DEMO"
    exp_group = 0
    sound_mode = 2
    # 사전 테스트
    print("\n📌 1단계: Note Identification Test (Before)")
    run_note_identification_test(num_questions=1, sub=sub, test_mode="baseline")

    # 자유 훈련 (1차)
    print("\n🎹 2단계: 자유 훈련 (1차)")
    run_piano_training(training_time=10, sound_mode=sound_mode, exp_group=exp_group)

    # instruction 기반 훈련
    print("\n🧠 3단계: Instruction 기반 훈련")
    run_instruction_training(sound_mode=sound_mode, exp_group=exp_group)

    # 자유 훈련 (2차)
    print("\n🎹 4단계: 자유 훈련 (2차)")
    run_piano_training(training_time=10, sound_mode=sound_mode, exp_group=exp_group)
    
    
    # 테스트 1 - 그룹별 음계 테스트
    print("\n✅ 4.5단계: Note Identification Test (GROUP)")
    run_note_identification_test(num_questions=3, sub=sub, test_mode="group", with_stim=True, exp_group=exp_group)

    # 테스트 2 - 공통 음계 테스트
    print("\n✅ 5단계: Note Identification Test (After)")
    run_note_identification_test(num_questions=3, sub=sub, test_mode="after", with_stim=False, exp_group=exp_group)

    print("\n🎉 실험 완료! 수고하셨습니다.")

if __name__ == "__main__":
    main()
