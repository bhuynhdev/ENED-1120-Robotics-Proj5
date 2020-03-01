#!/usr/bin/env python3

from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import MediumMotor, LargeMotor
from hello import debug_print


def medium_move_time(med_motor_name, power, seconds):
    med_motor_name.on_for_seconds(power, seconds)
    """i = 0
    while i <= 10:
        med_motor_name.on_for_seconds(power, seconds)
        med_motor_name.on_for_seconds(-power+20, seconds)
        i += 1"""

if __name__ == "__main__":
    pick_motor = MediumMotor(OUTPUT_B)
    pick_motor.on_for_seconds(-20, 1)
   
    
    