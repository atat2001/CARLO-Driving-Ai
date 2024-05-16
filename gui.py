# Imports
import numpy as np
from world import World
from agents import Car, RectangleBuilding, Painting, Pedestrian
from geometry import Point, Line
import time
from autonomous_agents import Greedy

DEBUG_ROAD_LINES = True # used to debug road lines

# Time steps (s)
dt = 5 

#World
world = World(dt, width = 300, height = 200, ppm = 3)

# Sidewalks
offset = 60
line = 1.5

dif_via = 5.5 # Length diferença entre vias (teste)


''' 
BLOCKS 
Comentário: já tiro o offset e lines para depois ser mais fácil vermos os limites à volta de cada intersection. 
Foi só mais fácil para mim no inicio para ver distancias e quês.
Also nao vale a pena por isto bonito, vai ficar assim
'''

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



''' TESTES '''

roads = {"0":[[20 + dif_via, 3], [20 + dif_via, 48]],
        "1":[[31, 53], [104, 53]],
        "2":[[104, 53 + dif_via],[31, 53 + dif_via]],
        "3":[[20 + dif_via, 64],[20 + dif_via, 117]],
        "4":[[20, 117],[20, 64]],
        "5":[[5, 53],[15, 53]],
        "6":[[15, 53 + dif_via],[5, 53 + dif_via]],
        "7":[[20, 48],[20, 3]],
        "8":[[109.5 + dif_via, 64],[109.5 + dif_via, 111]],
        "9":[[109.5, 111],[109.5, 64]],
        "10":[[31, 122.5],[104, 122.5]],
        "11":[[104, 122.5 + dif_via],[31, 122.5 + dif_via]],
        "12":[[20 + dif_via, 134],[20 + dif_via, 160]],
        "13":[[20, 160],[20, 134]],
        "14":[[31, 166],[104, 166]],
        "15":[[104, 166 + dif_via],[31, 166 + dif_via]],
        "16":[[109.5 + dif_via, 140],[109.5 + dif_via, 160]],
        "17":[[109.5, 160],[109.5, 140]],
        "18":[[172, 112 + dif_via*4],[121, 112 + dif_via*4]],
        "19":[[172, 112 + dif_via*3],[121, 112 + dif_via*3]],
        "20":[[121, 112 + dif_via*2],[172, 112 + dif_via*2]],
        "21":[[121, 112 + dif_via*1],[172, 112 + dif_via*1]],
        "22":[[172.5 + dif_via, 111],[172.5 + dif_via, 48]],
        "23":[[172.5 + dif_via*2, 111],[172.5 + dif_via*2, 48]],
        "24":[[172.5 + dif_via*3, 48],[172.5 + dif_via*3, 111]],
        "25":[[172.5 + dif_via*4, 48],[172.5 + dif_via*4, 111]],
        "26":[[200.5, 112 + dif_via],[251.5, 112 + dif_via]],
        "27":[[200.5, 112 + dif_via*2],[251.5, 112 + dif_via*2]],
        "28":[[251.5, 112 + dif_via*3],[200.5, 112 + dif_via*3]],
        "29":[[251.5, 112 + dif_via*4],[200.5, 112 + dif_via*4]],
        "30":[[172.5 + dif_via*4, 140],[172.5 + dif_via*4, 155]],
        "31":[[172.5 + dif_via*3, 140],[172.5 + dif_via*3, 155]],
        "32":[[172.5 + dif_via*2, 155],[172.5 + dif_via*2, 140]],
        "33":[[172.5 + dif_via, 155],[172.5 + dif_via, 140]],
        "34":[[200.5, 156 + dif_via],[251.5, 156 + dif_via]],
        "35":[[200.5, 156 + dif_via*2],[251.5, 156 + dif_via*2]],
        "36":[[251.5, 156 + dif_via*3],[200.5, 156 + dif_via*3]],
        "37":[[251.5, 156 + dif_via*4],[200.5, 156 + dif_via*4]],
        "38":[[252.5 + dif_via, 155],[252.5 + dif_via, 140]],
        "39":[[252.5 + dif_via*2, 155],[252.5 + dif_via*2, 140]],
        "40":[[252.5 + dif_via*3, 140],[252.5 + dif_via*3, 155]],
        "41":[[252.5 + dif_via*4, 140],[252.5 + dif_via*4, 155]],
        "42":[[252.5 + dif_via, 111],[252.5 + dif_via, 48]],
        "43":[[252.5 + dif_via*2, 111],[252.5 + dif_via*2, 48]],
        "44":[[252.5 + dif_via*3, 48],[252.5 + dif_via*3, 111]],
        "45":[[252.5 + dif_via*4, 48],[252.5+ dif_via*4, 111]],
        "46":[[251.5, 19.5 + dif_via*4],[200.5, 19.5 + dif_via*4]],
        "47":[[251.5, 19.5 + dif_via*3],[200.5, 19.5 + dif_via*3]],
        "48":[[200.5, 19.5 + dif_via*2],[251.5, 19.5 + dif_via*2]],
        "49":[[200.5, 19.5 + dif_via],[251.5, 19.5 + dif_via]],
        }

# Teste Cars
c1 = Car(Point(20, 20), np.pi/2)

c2 = Car(Point(25.5, 20), np.pi/2)
autonomous_list = []
autonomous_list.append(Greedy(c2,["0","1","8","11","4", "1", "8", "20", "27", "42", "47"]))

for road in roads:
    goal = roads[road]
    start = goal[0]
    end = goal[1]
    if DEBUG_ROAD_LINES:
        world.add(Line(Point(start[0], start[1]), Point(end[0], end[1])))   
    #world.add(Pedestrian(Point(start[0], start[1]), np.pi))
    #world.add(Pedestrian(Point(end[0], end[1]), np.pi))

world.add(c1)
world.add(c2)

world.render()
from interactive_controllers import KeyboardController
controller = KeyboardController(world)
#autonomous_list[0].do_left_turn()
# Move C1 -> example_intersection.py 
while True:
    c1.set_control(controller.steering, controller.throttle)
    for aut in autonomous_list:
        aut.update()
    world.tick() 
    world.render()
    time.sleep(dt/4000) 
    
    if world.collision_exists(): 
        print('Collision exists somewhere...')

world.close()
