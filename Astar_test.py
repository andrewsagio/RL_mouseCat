# run this file after main.py
# In ipython:
# %run main.py
# %run -i Astar_test.py

import Astar

the_map = world.getMap()

n = len(the_map[0]) # num cols
m = len(the_map) # num rows
dirs = directions # number of allowable movement directions, eg. 8
dx, dy = world.getdxdy()

xA = cat.cell.x
yA = cat.cell.y

xB = mouse.cell.x
yB = mouse.cell.y



route = Astar.pathFind(the_map, n, m, dirs, dx, dy, xA, yA, xB, yB)