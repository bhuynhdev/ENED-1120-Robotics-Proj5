#!/usr/bin/env python3

from ev3dev2.motor import MoveSteering, OUTPUT_A, OUTPUT_D
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import GyroSensor
from time import sleep, time
from hello import debug_print



def reset_gyro(gyro_sensor_name):
# Reset gyro sensor by switch to Rate mode then back to Angle mode
    gyro_sensor_name.mode = 'GYRO-RATE'
    gyro_sensor_name.mode = 'GYRO-ANG'


def debug_gyro(gyro_sensor_name):
    reset_gyro(gyro_sensor_name)
    while True:
        debug_print(gyro_sensor_name.angle)

def turn90_left(gyro_sensor_name, steer_pair_name):
    while True:
        angle_positive = abs(gyro_sensor_name.angle)
        debug_print(gyro_sensor_name.angle)
        steer_pair_name.on(steering=100, 
                           speed = 23 - round(angle_positive / 6))                            
        if (angle_positive >= 79):
            steer_pair_name.off()
            break
    return


def main():
    steer_pair = MoveSteering(OUTPUT_D, OUTPUT_A)
    gyro_sensor = GyroSensor(INPUT_2)

    reset_gyro(gyro_sensor)
    turn90_left(gyro_sensor, steer_pair)

if __name__ == "__main__":
    gyro_sensor = GyroSensor(INPUT_2)
    debug_gyro(gyro_sensor)