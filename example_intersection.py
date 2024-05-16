import numpy as np
from world import World
from agents import Car, RectangleBuilding, Pedestrian, Painting
from geometry import Point
import time
import traceback
from autonomous_agents import Greedy
human_controller = True


"""
# Let's also add some zebra crossings, because why not.
w.add(Painting(Point(18, 81), Point(0.5, 2), 'white'))
w.add(Painting(Point(19, 81), Point(0.5, 2), 'white'))
w.add(Painting(Point(20, 81), Point(0.5, 2), 'white'))
w.add(Painting(Point(21, 81), Point(0.5, 2), 'white'))
w.add(Painting(Point(22, 81), Point(0.5, 2), 'white'))
"""

dt = 5 # time steps in terms of seconds. In other words, 1/dt is the FPS.
w = World(dt, width = 300, height = 200, ppm = 3) # The world is 120 meters by 120 meters. ppm is the pixels per meter.
autonomous_list = []


# Sidewalks
offset = 60
line = 1.5
world = w

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

#9# Time steps (s)
dt = 5 
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

# A Car object is a dynamic object -- it can move. We construct it using its center location and heading angle.
c1 = Car(Point(20,20), np.pi/2)
w.add(c1)


goals = [[120,90], [120,117], [126,125], [158,125], [164,131],[164,161]]
#goals = [[120,90],[120,100], [140,130]]
c2 = Car(Point(120,90), np.pi/2, 'blue')

autonomous_list.append(Greedy(c2,goals))
#c2.velocity = Point(1.5,0) # We can also specify an initial velocity just like this.
w.add(c2)


## add goal points
for goal in goals:
    p1 = Pedestrian(Point(goal[0], goal[1]), np.pi)
    w.add(p1)

w.render() # This visualizes the world we just constructed.


## nunca entra aqui
if not human_controller:
    # Let's implement some simple scenario with all agents
    p1.set_control(0, 0.22) # The pedestrian will have 0 steering and 0.22 throttle. So it will not change its direction.
    c1.set_control(0, 0.35)
    c2.set_control(0, 0.05)
    for k in range(400):
        # All movable objects will keep their control the same as long as we don't change it.
        if k == 100: # Let's say the first Car will release throttle (and start slowing down due to friction)
            c1.set_control(0, 0)
        elif k == 200: # The first Car starts pushing the brake a little bit. The second Car starts turning right with some throttle.
            c1.set_control(0, -0.02)
        elif k == 325:
            c1.set_control(0, 0.8)
            #c2.set_control(-0.45, 0.3)
        elif k == 367: # The second Car stops turning.
            continue#c2.set_control(0, 0.1)
        w.tick() # This ticks the world for one time step (dt second)
        w.render()
        time.sleep(dt/4) # Let's watch it 4x

        if w.collision_exists(p1): # We can check if the Pedestrian is currently involved in a collision. We could also check c1 or #c2.
            print('Pedestrian has died!')
        elif w.collision_exists(): # Or we can check if there is any collision at all.
            print('Collision exists somewhere...')
    w.close()

else: # Let's use the steering wheel (Logitech G29) for the human control of car c1
    p1.set_control(0, 0.22) # The pedestrian will have 0 steering and 0.22 throttle. So it will not change its direction.
    #c2.set_control(0, 0.35) 
    from interactive_controllers import KeyboardController
    controller = KeyboardController(w)
    #autonomous_list[0].do_left_turn()
    while True:

        c1.set_control(controller.steering, controller.throttle)
        for aut in autonomous_list:
            aut.mock_update()
        w.tick() # This ticks the world for one time step (dt second)
        w.render()
        time.sleep(dt/4000) # Isto é tipo a accuracy das coisas, quanto maior for esse numero mais updates dá
        if w.collision_exists() and False:
            print('Collision exists somewhere...')
            






""" not needed anymore
    #points = [[118,90],[],[],[]]
        if a and abs(c2.heading -np.pi) < 0.0005:
            z = z + 1
            if z == 10:
                for x in range(len(points)-1):
                    print([points[x+1][0] - points[x][0], points[x+1][1] - points[x][1]])
                print([points[0][0] - points[3][0], points[0][1] - points[3][1]])
                print(points)
                print("done")
                exit()
        if abs(c2.heading -(np.pi/2)) < 0.0005:
            i = 3
            if points[i] == []:
                points[i] = [c2.center.x,c2.center.y]
            points[i] = [(c2.center.x+points[i][0])/2,(c2.center.y+points[i][1])/2]

        if abs(c2.heading -(3*np.pi/2)) < 0.0005:
            i = 1
            if points[i] == []:
                points[i] = [c2.center.x,c2.center.y]
            points[i] = [(c2.center.x+points[i][0])/2,(c2.center.y+points[i][1])/2]

        if abs(c2.heading) < 0.0005:
            i = 2
            if points[i] == []:
                points[i] = [c2.center.x,c2.center.y]
            points[i] = [(c2.center.x+points[i][0])/2,(c2.center.y+points[i][1])/2]
"""