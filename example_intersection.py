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
w = World(dt, width = 400, height = 300, ppm = 3) # The world is 120 meters by 120 meters. ppm is the pixels per meter.
autonomous_list = []
# Let's add some sidewalks and RectangleBuildings.
# A Painting object is a rectangle that the vehicles cannot collide with. So we use them for the sidewalks.
# A RectangleBuilding object is also static -- it does not move. But as opposed to Painting, it can be collided with.
# For both of these objects, we give the center point and the size.

w.add(Painting(Point(71.5, 106.5), Point(97, 27), 'gray80')) # We build a sidewalk.
w.add(RectangleBuilding(Point(72.5, 107.5), Point(95, 25))) # The RectangleBuilding is then on top of the sidewalk, with some margin.

# Let's repeat this for 4 different RectangleBuildings.
w.add(Painting(Point(8.5, 106.5), Point(17, 27), 'pink'))
w.add(RectangleBuilding(Point(7.5, 107.5), Point(15, 25)))

w.add(Painting(Point(8.5, 41), Point(17, 82), 'gray80'))
w.add(RectangleBuilding(Point(7.5, 40), Point(15, 80)))

offset = 6
w.add(Painting(Point(71.5+offset, 41), Point(97+offset, 82), 'blue'))
w.add(RectangleBuilding(Point(72.5+offset, 40), Point(95+offset, 80)))


# A Car object is a dynamic object -- it can move. We construct it using its center location and heading angle.
c1 = Car(Point(20,20), np.pi/2)
w.add(c1)

c2 = Car(Point(118,90), np.pi, 'blue')

autonomous_list.append(Greedy(c2,[[1,2,3]]))
#c2.velocity = Point(1.5,0) # We can also specify an initial velocity just like this.
w.add(c2)

# Pedestrian is almost the same as Car. It is a "circle" object rather than a rectangle.
p1 = Pedestrian(Point(28,81), np.pi)
p1.max_speed = 10.0 # We can specify min_speed and max_speed of a Pedestrian (and of a Car). This is 10 m/s, almost Usain Bolt.
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
        if w.collision_exists():
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