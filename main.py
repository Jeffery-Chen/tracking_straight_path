#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" main script """

import vrepInterface
import imageProcessing
import config
import numpy as np
import vrep
import time

theta_p = 0
theta_sum = 0

def motion(dev,theta):
    # move the wheels. Input: Angular velocities in rad/s
    l_dist, r_dist = np.random.normal(config.dist_mean, config.dist_var, size=2)  # random interference
    vrepInterface.move_wheels(config.speed - config.Kp1*dev - (config.Kp2*theta+config.Ki2*theta_sum+config.Kd2*(theta-theta_p)) + l_dist,
                              config.speed + config.Kp1*dev + (config.Kp2*theta+config.Ki2*theta_sum+config.Kd2*(theta-theta_p)) + r_dist)

def run():
    vrepInterface.connect()
    vrepInterface.start()
    vrepInterface.move_wheels(config.speed, config.speed)

    while (vrep.simxGetConnectionId(vrepInterface.clientID) != -1):
        global theta_p, theta_sum
        A0, B0, C0 = imageProcessing.preIP()
        dev = imageProcessing.get_dev(A0, B0, C0)
        theta = imageProcessing.get_theta(A0, B0)
        if abs(dev) > config.tolerance or abs(theta) > config.angle:
            motion(dev, theta)
            theta_sum = theta_sum + theta
            theta_p = theta
            print(dev,theta)
        else:
            l_dist, r_dist = np.random.normal(config.dist_mean, config.dist_var, size=2)  # random interference
            vrepInterface.move_wheels(config.speed + l_dist , config.speed + r_dist)
            print('no change')
    vrepInterface.stop()
    vrepInterface.disconnect()

if __name__ == "__main__":
    run()