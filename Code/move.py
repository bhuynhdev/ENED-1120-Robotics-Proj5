#!/usr/bin/env python3

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import MediumMotor, LargeMotor, MoveSteering
from hello import debug_print


left_wheel = LargeMotor(OUTPUT_D)
right_wheel = LargeMotor(OUTPUT_A)

medium = MediumMotor(OUTPUT_B)

steer_pair = MoveSteering(OUTPUT_D, OUTPUT_A)

while True:
    steer_pair.on_for_seconds(steering=0, speed=30, seconds=3)
    steer_pair.on_for_seconds(steering=0, speed=-30, seconds=3)
