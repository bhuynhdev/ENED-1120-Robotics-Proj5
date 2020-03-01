#!/usr/bin/env python3

from ev3dev2.motor import MoveSteering, OUTPUT_A, OUTPUT_D
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import GyroSensor
from hello import debug_print
from time import time, sleep
from gyro_steer import reset_gyro, turn90_left


"""def forward1(steer_pair_name, gyro_sensor_name):
    while True:
        debug_print(gyro_sensor_name.angle)
        steer_pair_name.on((1)*gyro_sensor_name.angle , 15)"""

"""def forward2(tank_pair_name, gyro_sensor_name):
    left_speed = right_speed = 10
    while True:
        debug_print(gyro_sensor_name.angle)
        tank_pair_name.on(left_speed, right_speed)
        if (gyro_sensor_name.angle > 0):
            right_speed += 1
        elif (gyro_sensor_name.angle < 0):
            right_speed -= 1

def forward3(steer_pair_name, gyro_sensor_name):
    Kp = 0.3
    Ki = 0.0001
    Kd = 0.35
    integral = 0
    last_error = 0
    while True:
        error = gyro_sensor_name.angle * (-1)
        integral += error
        derivative = error - last_error
        correction = error * Kp + integral * Ki + derivative * Kd
        last_error = error
        steer_pair_name.on(correction, 15)"""


def forward_with_time(steer_pair_name, gyro_sensor_name, time_sec):
    startTime = time()
    Kp = -0.0149495
    Ki = 0.0001
    Kd = 0
    integral = 0
    last_error = 0
    while (time() - startTime <= time_sec):
        debug_print(time() - startTime)
        error = gyro_sensor_name.angle * (-1)
        integral += error
        derivative = error - last_error
        correction = error * Kp + integral * Ki + derivative * Kd
        last_error = error
        steer_pair_name.on(correction, 15)


def backward_with_time(steer_pair_name, gyro_sensor_name, time_sec):
    startTime = time()
    Kp = -0.0149494
    Ki = 0.0001
    Kd = 0
    integral = 0
    last_error = 0
    while (time() - startTime <= time_sec):
        debug_print(time() - startTime)
        error = gyro_sensor_name.angle * (-1)
        integral += error
        derivative = error - last_error
        correction = error * Kp + integral * Ki + derivative * Kd
        last_error = error
        steer_pair_name.on(correction, -15)

        


def main():
    steer_pair = MoveSteering(OUTPUT_D, OUTPUT_A)
    gyro_sensor = GyroSensor(INPUT_2)
    reset_gyro(gyro_sensor)
    # forward1(steer_pair, gyro_sensor)
    forward_with_time(steer_pair, gyro_sensor, time_sec=4.76) # Forward 60 cm
    sleep(2)
    backward_with_time(steer_pair, gyro_sensor, time_sec=4.45) # Backward 60cm 
    sleep(2)

    forward_with_time(steer_pair, gyro_sensor, time_sec=4.76) # Forward 60 cm
    sleep(2)
    backward_with_time(steer_pair, gyro_sensor, time_sec=4.45) # Backward 60cm 
    sleep(2)

    forward_with_time(steer_pair, gyro_sensor, time_sec=4.76) # Forward 60 cm
    sleep(2)
    backward_with_time(steer_pair, gyro_sensor, time_sec=4.45) # Backward 60cm 
    sleep(2)

    forward_with_time(steer_pair, gyro_sensor, time_sec=4.76) # Forward 60 cm
    sleep(2)
    backward_with_time(steer_pair, gyro_sensor, time_sec=4.45) # Backward 60cm 
    sleep(2) 


if __name__ == "__main__":
    main()
