# main.py
from GraduateThesisAP_train import run_piano_training

if __name__ == "__main__":
    run_piano_training(
        training_time=60,  # 훈련 시간(초)
        sound_mode=2,      # 1=hold, 2=hold_max_1s, 3=fixed_1s
        exp_group=1        # 0=CTRL, 1=ETACTILE
    )
