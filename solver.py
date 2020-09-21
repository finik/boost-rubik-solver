import color
import time
from rubik_solver import utils
import json
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

    def translate_moves(self, solution):
        state = {"F": "F", "R": "R", "L": "L", "D": "D", "U": "U", "B": "B"}
        

        def left():
            state["R"], state["F"], state["L"], state["B"] = state["F"], state["L"], state["B"], state["R"]
            return "l"
        def right():
            state["F"], state["L"], state["B"], state["R"] = state["R"], state["F"], state["L"], state["B"]
            return "r"
        def tilt():
            state["F"], state["U"], state["B"], state["D"] = state["D"], state["F"], state["U"], state["B"]
            return "t"
        def get_side(val): 
            for key, value in state.items(): 
                 if val == value: 
                     return key

        moves = []
        tilt () # we start with one tile after scanning
        while len(solution):
            m = solution.pop(0)
            direction = m[0]
            side = get_side(direction)
            if side == 'R':
                moves += [left(), tilt()]
            elif side == "L":
                moves += [right(), tilt()]
            elif side == "F":
                moves += [left(), left(), tilt()]
            elif side == "B":
                moves += [tilt()]
            elif side == "U":
                moves += [tilt(), tilt()]

            if len(m) == 1:
                moves.append("tr")
            elif m[1] == "'":
                moves.append("tl")
            elif m[1] == "2":
                moves.append("tl2")

        print(moves)
        return moves

    def execute(self, moves):
        while len(moves):
            m = moves.pop(0)
            print(f"Executing {m}")
            if m == 'l':
                self.boost.grip_down()
                self.boost.rotate(-1)
            elif m == 'r':
                self.boost.grip_down()
                self.boost.rotate(1)
            elif m == 'tr':
                self.boost.grip_up()
                self.boost.rotate(-1, True)
            elif m == 'tl':
                self.boost.grip_up()
                self.boost.rotate(1, True)
            elif m == 't':
                self.boost.tilt()
            elif m == 'tl2':
                self.boost.grip_up()
                self.boost.rotate(2, True)


    def patch_kociemba(self, state):
        state = state.upper()
        state = state.replace(state[4], 'y')
        state = state.replace(state[13], 'b')
        state = state.replace(state[22], 'r')
        state = state.replace(state[31], 'g')
        state = state.replace(state[40], 'o')
        state = state.replace(state[49], 'w')
        return state

    def solve(self):
        state = self.get_state()
        normalized_kociemba = self.patch_kociemba(state)
        print(state, normalized_kociemba)
        solution = None
        try:
            solution = [str(x) for x in utils.solve(normalized_kociemba, 'Kociemba')]

        except:
            print("Error finding a solution, please retry")

        if solution:
            print(solution)
            moves = self.translate_moves(solution)
            self.execute(moves)

if __name__ == '__main__':
    solver = Solver(1, 2)
    s = "yyryyryyrbbbbbbbbbrrwrrwrrwgggggggggyooyooyoowwowwowwo"
    solution = [str(x) for x in utils.solve(s, 'Kociemba')]
    print(solution)
    moves = solver.translate_moves(solution)
    print(moves)

