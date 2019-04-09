#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" image processing """

import vrepInterface
import config
import cv2
import numpy as np
import math
import sys

A0=1
B0=1
C0=1
lines_past=np.zeros(shape=(2,1,2))

def preIP():
    global A0, B0, C0, lines_past
    mdist = 0.2
    img = vrepInterface.read_image()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    #lines = cv2.HoughLinesP(edges, 1, np.pi / 180,config.threshold, config.minLineLength, config.maxLineGap)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
    if np.all(lines):
        lines=lines_past
    [groups, rows, cols] = lines.shape
    lines_past=lines
    for i in range(groups-1):
        rho = lines[i,0,0]
        theta = lines[i,0,1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 512 * (-b))
        y1 = int(y0 + 512 * (a))
        x2 = int(x0 - 512 * (-b))
        y2 = int(y0 - 512 * (a))
        if x1 == x2 or y1 > 450 or y2 > 450:
            continue
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        A = y2 - y1
        B = x1 - x2
        C = x2 * y1 - x1 * y2
        dist = (A * 256 + B * 256 + C) / math.sqrt(A ** 2 + B ** 2) / 1280  # '1280' is the scaling factor(map to sensor)
        if dist < mdist:
            mdist = dist
            A0 = A
            B0 = B
            C0 = C
    cv2.imshow("Image", img)
    cv2.waitKey(20)
    return A0, B0, C0

def get_dev(A0,B0,C0):
    dev=(A0*256+B0*256+C0)/math.sqrt(A0**2+B0**2)/1280
    return dev

def get_theta(A0,B0):
    theta=math.atan2(-A0,B0)/math.pi*180
    if theta > 90:
        theta = 180 - theta
    if theta < -90:
        theta = 180 + theta
    return theta