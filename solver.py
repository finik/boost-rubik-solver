from pylgbst.hub import MoveHub, COLORS, COLOR_NONE, COLOR_RED
from pylgbst import get_connection_bleak
import time
import logging

    
# logging.basicConfig(level=logging.WARN, format='%(relativeCreated)d\t%(levelname)s\t%(name)s\t%(message)s')
hub = MoveHub(get_connection_bleak(hub_mac = "D8EED5BD-D9DA-43C5-97E1-4273F0368182"))


QUARTER_TURN = 90

RTURN_OVERSHOOT = 24
LTURN_OVERSHOOT = 19

GRIP_TURN = 90
ROD_TURN = 70

class Solver():
    def __init__(self):
        self.grip = None
        
    def rotate_table_cw(self, overshoot = 0):
        res = hub.motor_external.angled(QUARTER_TURN+overshoot, 0.1)
        if overshoot:
            res &= hub.motor_external.angled(-overshoot, 1)
        return res
            
    def rotate_table_ccw(self, overshoot = 0):
        res = hub.motor_external.angled(-(QUARTER_TURN+overshoot), 0.1)
        if overshoot:
            res &= hub.motor_external.angled(overshoot, 1)
        return res
        
    def grip_up(self):
        if self.grip == True:
            return True
        res = hub.motor_B.angled(-GRIP_TURN, 0.2)
        self.grip = True
        return res
        
    def grip_down(self):
        if self.grip == False:
            return
        res = hub.motor_B.angled(GRIP_TURN, 0.2)
        self.grip = False
        return res
        
    
    def tilt(self):
        self.grip_down()
        res = hub.motor_A.angled(-ROD_TURN, 0.2)
        res &= hub.motor_A.angled(ROD_TURN, 0.5)
        self.grip_up()
        return res
        

print("Avaliable commands:")
print("r   - rotate bed clockwise")
print("l   - rotate bed counter-clockwise")
print("t   - tilt")
print("gu  - grip up")
print("gd  - grip down")
print("q   - exit")

solver = Solver()

while True:
    cmd = input("Enter your command: ")
    res = None
    if cmd == "r":
        res = solver.rotate_table_cw(RTURN_OVERSHOOT)
    elif cmd == "l":
        res = solver.rotate_table_ccw(LTURN_OVERSHOOT)
    elif cmd == "gu":
        res = solver.grip_up()
    elif cmd == "gd":
        res = solver.grip_down()
    elif cmd == "t":
        res = solver.tilt()
    elif cmd == "q":
        hub.switch_off()
        time.sleep(2)
        break
    else:
        print("Unknown command")
        
    if res:
        print("Command successfull")
    elif res == False:
        print("Command failed!")