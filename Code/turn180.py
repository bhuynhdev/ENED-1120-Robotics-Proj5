#!/usr/bin/env python3

from ev3dev2.motor import MoveSteering, OUTPUT_A, OUTPUT_D
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import GyroSensor
from gyro_steer import reset_gyro, turn90_left
from straight_gyro import forward_with_time


def turn180(steer_pair_name, gyro_sensor_name):
    while True:
        angle_positive = abs(gyro_sensor_name.angle)
        steer_pair_name.on(steering=100, 
                           speed = 46 - round(angle_positive / 6))                            
        if (angle_positive >= 172):
            steer_pair_name.off()
            break
    return


def main():
    steer_pair = MoveSteering(OUTPUT_D, OUTPUT_A)
    gyro_sensor = GyroSensor(INPUT_2)
    reset_gyro(gyro_sensor)
    forward_with_time(steer_pair, gyro_sensor, time_sec=5)
    turn180(steer_pair, gyro_sensor)
    reset_gyro(gyro_sensor)

    forward_with_time(steer_pair, gyro_sensor, time_sec=5)
    turn180(steer_pair, gyro_sensor)
    reset_gyro(gyro_sensor)

    forward_with_time(steer_pair, gyro_sensor, time_sec=5)
    turn180(steer_pair, gyro_sensor)
    reset_gyro(gyro_sensor)

    forward_with_time(steer_pair, gyro_sensor, time_sec=5)
    turn180(steer_pair, gyro_sensor)
    reset_gyro(gyro_sensor)



if __name__ == "__main__":
    main()
