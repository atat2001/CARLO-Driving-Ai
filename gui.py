# Imports
from world import World
from agents import Car, RectangleBuilding, Painting
from geometry import Point, Line
from shared_variables import roads, dt, paths
from autonomous_agents.passive import Passive
from autonomous_agents.greedy import Greedy
from autonomous_agents.social import Social
from autonomous_agents.phase_agent import PhaseAgent
import random

DEBUG_ROAD_LINES = True # used to debug road lines
TIME = 30               # time in seconds
N_MAX_CARS = 10

# World
world = World(dt, width = 300, height = 200, ppm = 3)

# Sidewalks
offset = 60
line   = 1.5


''' BLOCKS '''
#1
world.add(Painting(Point(8, 125.5), Point(17, 127), 'gray80'))
world.add(RectangleBuilding(Point(8 - line, 125.5 + line), Point(17 - line, 127 - line)))

#2
world.add(Painting(Point(7+offset, 90.5), Point(17+offset, 57), 'gray80')) 
world.add(RectangleBuilding(Point(5.5 + offset + line, 89 + line), Point(13.5 + offset - line, 53.5 - line))) 

#3
world.add(Painting(Point(8, 7 + line), Point(17, 82 + line), 'gray80'))
world.add(RectangleBuilding(Point(8 - line, 7), Point(17 - line, 82)))

#4
world.add(Painting(Point(146, 49.5), Point(55, 127), 'gray80')) 
world.add(RectangleBuilding(Point(144.5 + line, 48 + line), Point(51.5 - line, 123.5 - line))) 

#5
world.add(Painting(Point(14.5 + offset, 7 + line), Point(30 + offset + line, 82 + line), 'gray80'))
world.add(RectangleBuilding(Point(14.5 + offset+line, 7), Point(30 + offset, 82)))

# 6 e 7
world.add(Painting(Point(146, 173), Point(55, 69), 'gray80')) #6
world.add(Painting(Point(226, 148), Point(55, 19), 'gray80')) #7

#8
world.add(Painting(Point(90, 201), Point(150, 49), 'gray80'))
world.add(RectangleBuilding(Point(75, 220), Point(155, 82)))

#13
world.add(Painting(Point(230, 207), Point(200, 49), 'gray80'))
world.add(RectangleBuilding(Point(215, 226), Point(205, 82)))

#9
world.add(Painting(Point(7 + offset, 147), Point(17 + offset, 30), 'gray80')) 
world.add(RectangleBuilding(Point(5.5 + offset + line, 145.5 + line), Point(13.5 + offset - line, 26.5-line)))

# 6 e 7
world.add(RectangleBuilding(Point(144.5 + line, 171.5 + line), Point(51.5 - line, 65.5-line))) #6
world.add(RectangleBuilding(Point(224.5 + line, 146.5 + line), Point(51.5 - line, 15.5-line))) #7

#10
world.add(Painting(Point(226, 79.5), Point(55, 67), 'gray80')) 
world.add(RectangleBuilding(Point(224.5 + line, 78 + line), Point(51.5 - line, 63.5-line))) 

#11
world.add(Painting(Point(178 + offset + line, 4 + line), Point(70 + offset + line, 29 + line), 'gray80'))
world.add(RectangleBuilding(Point(175 + offset + line, 4), Point(70 + offset + line, 29)))

#12
world.add(Painting(Point(291, 101), Point(25, 164.5), 'gray80'))
world.add(RectangleBuilding(Point(291 + line, 100.5), Point(25 - line*1.5, 175.5)))

for road in roads:
    goal  = roads[road]
    start = goal[0]
    end   = goal[1]
    if DEBUG_ROAD_LINES:
        world.add(Line(Point(start[0], start[1]), Point(end[0], end[1])))


''' TESTES'''

autonomous_agents = []

# Testes Passive
for path in paths:
    car = Car()     
    autonomous_agents.append(Social(car, path, 1))
    

world.render()

world.run(autonomous_agents, N_MAX_CARS)

world.close()
