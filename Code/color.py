#!/usr/bin/env python3

from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1
from hello import debug_print


scanner = ColorSensor(INPUT_1)

while True:
    reflect = scanner.reflected_light_intensity
    debug_print(reflect)