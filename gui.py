# Imports
import numpy as np
from world import World
from agents import Car, RectangleBuilding, Painting
from geometry import Point
import time


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
world.add(Painting(Point(146, 163), Point(55, 49), 'gray80')) #6
world.add(Painting(Point(226, 148), Point(55, 19), 'gray80')) #7

#8
world.add(Painting(Point(165, 201), Point(300, 49), 'gray80'))
world.add(RectangleBuilding(Point(150, 220), Point(305, 82)))

#9
world.add(Painting(Point(7 + offset, 147), Point(17 + offset, 30), 'gray80')) 
world.add(RectangleBuilding(Point(5.5 + offset + line, 145.5 + line), Point(13.5 + offset - line, 26.5-line)))

# 6 e 7
world.add(RectangleBuilding(Point(144.5 + line, 161.5 + line), Point(51.5 - line, 45.5-line))) #6
world.add(RectangleBuilding(Point(224.5 + line, 146.5 + line), Point(51.5 - line, 15.5-line))) #7

#10
world.add(Painting(Point(226, 79.5), Point(55, 67), 'gray80')) 
world.add(RectangleBuilding(Point(224.5 + line, 78 + line), Point(51.5 - line, 63.5-line))) 

#11
world.add(Painting(Point(178 + offset + line, 4 + line), Point(70 + offset + line, 43 + line), 'gray80'))
world.add(RectangleBuilding(Point(175 + offset + line, 4), Point(70 + offset + line, 43)))

#12
world.add(Painting(Point(291, 102), Point(25, 153.5), 'gray80'))
world.add(RectangleBuilding(Point(291 + line, 102.5), Point(25 - line*1.5, 154.5)))

world.render()



''' TESTES '''
# Teste Cars
c1 = Car(Point(20, 20), np.pi/2)
c2 = Car(Point(20, 20), np.pi/2)
c3 = Car(Point(20 + dif_via, 20), np.pi/2)

c4 = Car(Point(172.5 + dif_via, 150), np.pi/2)
c5 = Car(Point(172.5 + dif_via*2, 150), np.pi/2)
c6 = Car(Point(172.5 + dif_via*3, 150), np.pi/2)
c7 = Car(Point(172.5 + dif_via*4, 150), np.pi/2)

world.add(c1)
world.add(c2)
world.add(c3)
world.add(c4)
world.add(c5)
world.add(c6)
world.add(c7)


# Move C1 -> example_intersection.py 
c1.set_control(0, 0.35)    
for k in range(400):    
    if k == 100: 
        c1.set_control(0, 0)
    elif k == 200: 
        c1.set_control(0, -0.02)
    elif k == 325:
        c1.set_control(0, 0.8)            
    elif k == 367: 
        continue
    world.tick() 
    world.render()
    time.sleep(dt/4) 
    
    if world.collision_exists(): 
        print('Collision exists somewhere...')

world.close()
