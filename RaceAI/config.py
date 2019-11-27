# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:58:26 2019

@author: shume
"""
#degree the car turn every time turn right or turn left event occurs
THETA = 1.8
DRIFT_THETA = 3

DRIFT_OFFSET = 8

DRIFT_INITIAL = 12

#accelation increase amount every time accelerator is pressed
A = 3
Amax = 0.15

#flat deceleration due to resistance
NA = 0.06

#deceleration due to braking
B = -0.25


