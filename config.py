#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" parameters setting """

kernelsize = 3      # smooth kernel
threshold = 10
minLineLength = 100 # HoughLines Minimum length
maxLineGap = 10     # HoughLines Maximum allowed gap between line segments to treat them as single line
speed = 0.5         # rad/s (pioneer 3dx: 0.5 rad/s: ~ 0.05m/s)
dist_mean = 0
dist_var = 0.025      # random interference factor (roughly ±2%)
tolerance = 0.001     # Position accuracy
angle = 1           # Angle accuracy (degree/°) Wheel radius roughly 0.095m
Kp1 = 8          # Wheel speed factor for dev
Kp2 = 0.0075          # Wheel speed factor for theta
Ki2 = 0.0005
Kd2 = 0.005
time_step = 0.05
wait_response = False