# main.py
from GraduateThesisAP_train import run_piano_training
from GraduateThesisAP_test import run_note_identification_test

sub = input("SUBJECT INITIAL: ")

exp_group = int(input("CHOOSE MODE (CTRL-0 ETACTILE-1): "))
exp_group = float(exp_group)

sound_mode = int(input("SOUND MODE (1=hold, 2=hold_max_1s, 3=fixed_1s): "))

if __name__ == "__main__":
    run_note_identification_test(5, sub)

    run_piano_training(
        training_time=60,  # 훈련 시간(초)
        sound_mode=sound_mode,      # 1=hold, 2=hold_max_1s, 3=fixed_1s
        exp_group=exp_group        # 0=CTRL, 1=ETACTILE
    )

    run_note_identification_test(5, sub)

    
