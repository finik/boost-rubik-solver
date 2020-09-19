#!/usr/bin/env python3


import time
import sys
import cv2
from color import name_to_bgr, detect_bgr, rect_average
import json
import threading
import color

REGION_SIZE = 32
REGION_PAD = 192
PREVIEW_SIZE = 64
PREVIEW_CUBE_SIZE = PREVIEW_SIZE*3
PREVIEW_X = 1020
PREVIEW_Y = 220
PREVIEW_SIDE_OFFSETS = [
    [PREVIEW_X+PREVIEW_CUBE_SIZE+20, PREVIEW_Y-PREVIEW_CUBE_SIZE-5],
    [PREVIEW_X, PREVIEW_Y],
    [PREVIEW_X+PREVIEW_CUBE_SIZE+5, PREVIEW_Y],
    [PREVIEW_X+PREVIEW_CUBE_SIZE*2+10, PREVIEW_Y],
    [PREVIEW_X+PREVIEW_CUBE_SIZE*3+15, PREVIEW_Y],
    [PREVIEW_X+PREVIEW_CUBE_SIZE+20, PREVIEW_Y+PREVIEW_CUBE_SIZE+5]
]

class Webcam:
    def __init__(self):
        self.update_state()
        print(PREVIEW_SIDE_OFFSETS)

    def draw_regions(self, frame):
        cv2.rectangle(frame, (960,0), (1920, 1080), (0, 0, 0), -1)
        for index in range(9):
            x, y = self.regions[index]
            rect  = frame[y:y+REGION_SIZE, x:x+REGION_SIZE]
            cv2.rectangle(frame, (x,y), (x+REGION_SIZE, y+REGION_SIZE), (255, 255, 255), 2)

            color = detect_bgr(rect_average(rect))[0]
            

    def draw_state(self, frame):
        for side in range(6):
            offsetx, offsety = PREVIEW_SIDE_OFFSETS[side]
            for y in range(3):
                for x in range(3):
                    color = self.state[side*9 + y*3 + x]
                    cv2.rectangle(frame,
                        (offsetx+x*PREVIEW_SIZE, offsety+y*PREVIEW_SIZE),
                        (offsetx+x*PREVIEW_SIZE+PREVIEW_SIZE, offsety+y*PREVIEW_SIZE+PREVIEW_SIZE),
                        name_to_bgr(color), -1)

    def update_window(self, frame):
        self.draw_regions(frame)
        self.draw_state(frame)
        height, width, layers =  frame.shape
        resize = cv2.resize(frame, (width//2, height//2)) 
        cv2.imshow("win1", resize)


    def update_state(self, state = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"):
        self.state = state

    def video_loop(self):
        self.cam = cv2.VideoCapture(0)
        cv2.namedWindow("win1");
        cv2.moveWindow("win1", 20, 20);
        while self.running:
            ret, frame = self.cam.read()
            key = cv2.waitKey(10) & 0xff
            if ret:
                self.current_frame = frame.copy()
                self.update_window(frame)

        self.cam.release()
        cv2.destroyAllWindows()

    def start_video(self):
        self.running = True
        self.regions = []
        for y in range(3):
            for x in range(3):
                self.regions.append([220+x*(REGION_SIZE+REGION_PAD), 220+y*(REGION_SIZE+REGION_PAD)])
                
        self.video_loop()

    def stop_video(self):
        self.running = False

    def scan(self):
        state = []
        for index, (x,y) in enumerate(self.regions):
            rect  = self.current_frame[y:y+REGION_SIZE, x:x+REGION_SIZE]
            state.append(color.rect_average(rect))
        return state   

        return None

