# from GraduateThesisAP_test import run_note_identification_test
from test import run_note_identification_test
from train_free import run_piano_training
from train_inst import run_instruction_training
from utils.serial_utils import init_serial, send_period


def main():
    print("🎓 E-Tactile Absolute Pitch Training 시작")

    # 사용자 정보 입력
    '''
    sub = input("SUBJECT INITIAL: ")
    exp_group = int(input("CHOOSE MODE (CTRL-0, ETACTILE-1): "))
    sound_mode = int(input("SOUND MODE (1=hold, 2=hold_max_1s, 3=fixed_1s): "))
    '''

    sub = "prof_DEMO_arduino"
    exp_group = 1
    sound_mode = 2

    # 호출부
    ser = init_serial(exp_group)  # 내부에서 알아서 판단


    # 사전 음계 테스트
    print("\n📌 1단계: 사전 음계 테스트")
    run_note_identification_test(
        num_questions=3,
        sub=sub,
        mode="test",        # 순수 청각 테스트
        ser=None           
    )

    # 자유 훈련 (1차)
    print("\n🎹 2단계: 자유 훈련")
    run_piano_training(training_time=60, sound_mode=2, ser=ser)

    # 지침 훈련
    print("\n🧠 3단계: 지침 훈련")
    run_instruction_training(
        sound_mode=2,
        ser=ser
    )

    # 자유 훈련 (2차)
    print("\n🎹 4단계: 자유 훈련")
    run_piano_training(training_time=60, sound_mode=2, ser=ser)

    # 🧘 5분 휴식
    print("\n⏸ 5분간 휴식입니다. 편하게 쉬고 오세요!")
    print("💡 다시 시작할 준비가 되면 ENTER 키를 눌러주세요.")
    input("▶ ENTER를 눌러 다음 단계로 진행: ")

    # 사후 테스트 : 요기가 validation
    # run_note_identification_test(num_questions=3, sub=sub, test_mode="group", with_stim=True, exp_group=exp_group)

    print("\n✅ 4.5단계: Note Identification Test (GROUP)")
    run_note_identification_test(
        num_questions=3,
        sub=sub,
        mode="validation",        # mode가 validation이면 그룹 1만 자극 받음
        ser=ser            
    )


    # 🧘 5분 휴식
    print("\n⏸ 5분간 휴식입니다. 편하게 쉬고 오세요!")
    print("💡 다시 시작할 준비가 되면 ENTER 키를 눌러주세요.")
    input("▶ ENTER를 눌러 다음 단계로 진행: ")

    # 테스트 2 : 요기가 test
    # run_note_identification_test(num_questions=3, sub=sub, test_mode="after", with_stim=False, exp_group=exp_group)

    print("\n✅ 5단계: Note Identification Test (After)")
    run_note_identification_test(
        num_questions=3,
        sub=sub,
        mode="test",        # 순수 청각 테스트
        ser=None           
    )


    print("\n🎉 실험 완료! 수고하셨습니다.")

if __name__ == "__main__":
    main()



