import cv2
import numpy as np
import win32api, win32con
from PIL import ImageGrab
import time
import imutils

print("6")
time.sleep(1)
print("5")
time.sleep(1)
print("4")
time.sleep(1)
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)

starttime = time.time()
m_x = 960
m_y = 540

while True:
    ball_list = []
    total = []
    endtime = time.time()
    nowtime = endtime - starttime


    im = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))
    #im = cv2.imread("aimlab.png")
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    lower = np.array([45,100,50])
    upper = np.array([75,255,255])

    mask = cv2.inRange(hsv, lower, upper)
    green = cv2.bitwise_and(im,im,mask = mask)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        #print(cX)
        total.append(int(((cX - m_x) ** 2 + (cY - m_y) ** 2) ** (1 / 2)))
        ball_list.append([cX, cY])

    index = np.argmin(total)
    cX = ball_list[index][0]
    cY = ball_list[index][1]

    cv2.drawContours(im, [c], -1, (0, 255, 255), 1)
    cv2.circle(im, (cX, cY), 1, (255, 255, 255), 3)
    #mouse.move(100, 500)
    #m_x, m_y = pyautogui.position()
    #print(m_x,m_y)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 2*(cX-m_x), 2*(cY-m_y), 0, 0)

    if(float(nowtime)>0.09):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        starttime = time.time()

#cv2.imshow("mask",green)
#cv2.imshow("aimlab",im)
#cv2.waitKey(0)
