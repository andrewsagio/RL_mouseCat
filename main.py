import time
import random
import cellular
reload(cellular)
import qlearn_my as qlearn
import Astar
#import qlearn_mod_random as qlearn # to use the alternative exploration method
#import qlearn # to use standard exploration method
reload(qlearn)

#cellFile = 'maze.txt'
cellFile = 'waco.txt'
#cellFile = 'barrier2.txt'

directions = 8

lookdist = 2 # scope of mouse state, mose can only look +/- lookdist cells
lookcells = []
for i in range(-lookdist,lookdist+1):
    for j in range(-lookdist,lookdist+1):
        if (abs(i) + abs(j) <= lookdist) and (i != 0 or j != 0):
            lookcells.append((i,j))

def pickRandomLocation():
    while 1:
        x = random.randrange(world.width)
        y = random.randrange(world.height)
        cell = world.getCell(x, y)
        if not (cell.wall or len(cell.agents) > 0):
            return cell


class Cell(cellular.Cell):
    wall = False

    def colour(self):
        if self.wall:
            return 'black'
        else:
            return 'white'

    def load(self, data):
        if data == 'X':
            self.wall = True
        else:
            self.wall = False


class Cat(cellular.Agent):
    cell = None
    score = 0
    colour = 'orange'

    def __init__(self, mode='A*'):
        self.mode = mode
        if mode == 'A*':
            self.update = self.update_AStar
        else:
            self.update = self.update_default

    def update_default(self):
        ''' go towards mouse direction naviely '''
        cell = self.cell
        if cell != mouse.cell:
            self.goTowards(mouse.cell)
            if cell == self.cell:
                self.goInDirection(random.randrange(directions))

    def update_AStar(self):
        ''' Go to mouse using A* path finding algorithm'''
        the_map = world.getMap()
        n = len(the_map[0]) # num cols
        m = len(the_map) # num rows
        dirs = directions # number of allowable movement directions, eg. 8
        dx, dy = world.getdxdy()
        start = (self.cell.x, self.cell.y)
        goal = (mouse.cell.x, mouse.cell.y)
        route = Astar.pathFind2(the_map, dirs, dx, dy, start, goal)
        if route:
            self.goInDirection(int(route[0]))
        else:
            self.goInDirection(random.randrange(directions))






class Cheese(cellular.Agent):
    colour = 'yellow'

    def update(self):
        pass


class Mouse(cellular.Agent):
    colour = 'gray'

    def __init__(self):
        self.ai = None
        self.ai = qlearn.QLearn(actions=range(directions),
                                alpha=0.1, gamma=0.9, epsilon=0.1)
        self.eaten = 0
        self.fed = 0
        self.lastState = None
        self.lastAction = None

    def update(self):
        state = self.calcState()
        reward = -1

        if self.cell == cat.cell:
            self.eaten += 1
            reward = -100
            if self.lastState is not None:
                self.ai.learn(self.lastState, self.lastAction, reward, state)
            self.lastState = None

            self.cell = pickRandomLocation()
            return

        if self.cell == cheese.cell:
            self.fed += 1
            reward = 50
            cheese.cell = pickRandomLocation()

        if self.lastState is not None:
            self.ai.learn(self.lastState, self.lastAction, reward, state)

        state = self.calcState()  #
        action = self.ai.chooseAction(state)
        self.lastState = state
        self.lastAction = action

        self.goInDirection(action)

    def calcState(self):
        def cellvalue(cell):
            if cat.cell is not None and (cell.x == cat.cell.x and
                                         cell.y == cat.cell.y):
                return 3
            elif cheese.cell is not None and (cell.x == cheese.cell.x and
                                              cell.y == cheese.cell.y):
                return 2
            else:
                return 1 if cell.wall else 0

        return tuple([cellvalue(self.world.getWrappedCell(self.cell.x + j, self.cell.y + i))
                      for i,j in lookcells])


cat = Cat()
cat2 = Cat()
cheese = Cheese()
mouse = Mouse()

world = cellular.World(Cell, directions=directions, filename=cellFile)
world.age = 0

world.addAgent(cheese, cell=pickRandomLocation())
world.addAgent(cat)
#world.addAgent(cat2)
world.addAgent(mouse) # mouse needs to be at the end for proper display

endAge = world.age + 150000

t0 = time.time()
t = t0
while world.age < endAge:
    world.update()

    if world.age % 10000 == 0:
        t_last = t
        t = time.time()
        print "{:d}, e: {:0.2f}, W: {:d}, L: {:d}, T:{:0.1f}"\
            .format(world.age, mouse.ai.epsilon, mouse.fed, mouse.eaten, t - t_last)
        mouse.eaten = 0
        mouse.fed = 0

world.display.activate(size=30)
world.display.delay = 1
print '#Train time: ', time.time() - t0

while 1:
    world.update()