from pylgbst.hub import MoveHub, COLORS, COLOR_NONE, COLOR_RED
from pylgbst import get_connection_bleak
import time
import logging

QUARTER_TURN = 90

RTURN_OVERSHOOT = 24
LTURN_OVERSHOOT = -19

GRIP_TURN = 90
ROD_TURN = 80

class Boost():
    def __init__(self):
        self.grip = None
        self.hub = MoveHub(get_connection_bleak(hub_mac = "D8EED5BD-D9DA-43C5-97E1-4273F0368182"))
        
        
    def rotate(self, direction: int, overshoot: bool = False):
        overshoot_value = 0
        if overshoot:
            if direction > 0:
                overshoot_value = RTURN_OVERSHOOT
            else:
                overshoot_value = LTURN_OVERSHOOT

        print(direction*QUARTER_TURN + overshoot_value)
        res = self.hub.motor_external.angled(direction*QUARTER_TURN + overshoot_value, 0.1)
        if overshoot:
            res &= self.hub.motor_external.angled(-overshoot_value, 1)
        return res
        
    def grip_up(self):
        if self.grip == True:
            return True
        res = self.hub.motor_B.angled(-GRIP_TURN, 0.2)
        self.grip = True
        return res
        
    def grip_down(self):
        if self.grip == False:
            return
        res = self.hub.motor_B.angled(GRIP_TURN, 0.2)
        self.grip = False
        return res
        
    
    def tilt(self):
        self.grip_down()
        res = self.hub.motor_A.angled(-ROD_TURN, 0.2)
        res &= self.hub.motor_A.angled(ROD_TURN, 0.5)
        self.grip_up()
        return res

    def off(self):
        self.hub.switch_off()


