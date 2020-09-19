import color
import time
from rubik_solver import utils
from rubik_solver.CubieCube import DupedEdge

MOVE_MAP = {
    "R": ["l", "t", "tr", "r", "t", "l"],
    "R'": ["l", "t", "tl", "l", "t", "l"]

}

class Solver:
    def __init__(self, boost, webcam):
        self.boost = boost
        self.webcam = webcam

    def get_state(self):
        self.boost.grip_down()
        time.sleep(1)
        top = self.webcam.scan()
        
        
        self.boost.tilt()
        self.boost.grip_down()
        time.sleep(2)
        front = self.webcam.scan()

        self.boost.rotate(-1)
        time.sleep(1)
        left = self.webcam.scan()
        
        self.boost.rotate(-1)
        time.sleep(1)
        rear = self.webcam.scan()

        self.boost.rotate(-1)
        time.sleep(1)
        right = self.webcam.scan()

        self.boost.rotate(-1)
        time.sleep(1)
        self.boost.tilt()
        time.sleep(2)
        bottom = self.webcam.scan()

        state = list(map(lambda x: {"avg": x}, top + left + front + right + rear + bottom))
        print(state)
        colors = color.get_colors(state)
        print(colors)
        self.webcam.update_state(colors)

        return colors

    def calc_moves(self, solution):
        # Start with 3 titlts to get back to the original orienatation
        moves = ['t', 't', 't']
        return moves


    def execute(self, solution):
        pass

    def solve(self):
        state = self.get_state()
        normalized_kociemba = patch_kociemba(state)
        print(state, normalized_kociemba)
        try:
            solution = utils.solve(normalized_kociemba, 'Kociemba')
            print(solution)
            self.execute(solution)
        except:
            print("Error finding a solution, please retry")





def patch_kociemba(state):
    state = state.upper()
    state = state.replace(state[4], 'y')
    state = state.replace(state[13], 'b')
    state = state.replace(state[22], 'r')
    state = state.replace(state[31], 'g')
    state = state.replace(state[40], 'o')
    state = state.replace(state[49], 'w')
    return state