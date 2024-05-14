import numpy as np
from enum import Enum

LANE_DISTANCE = 5
GOAL_RADIUS = 2
SIDE_TURN = np.pi/15

class TypeObj(Enum):
    INTERSECTION_START = 1
    INTERSECTION_DECISION = 2
    INTERSECTION_END = 3

class objective:
    def __init__(self, position, heading, type_obj, intersection):
        self.position = position
        self.heading = heading
        self.type_obj = type_obj
        self.intersection = intersection

class Greedy:
    def __init__(self, car, path):
        self.path = path
        self.cur_goal = 0
        self.car = car
        self.car.debug = True
        self._steering = 0
        self._throttle = 0
        self.turning = [False, False]
        self.old_heading = None

    @property
    def steering(self):
        return self._steering
    @property
    def throttle(self):
        #print("going vruuum")
        return self._throttle

    @steering.setter
    def steering(self, val):
        self._steering = val
    @throttle.setter
    def throttle(self, val):
        print(self._throttle)
        self._throttle = val

    def accelerate(self):
        #print("vrum vrum")
        self.throttle = 1.5

    def deaccelerate(self):
        self.throttle = -1.5

    def _turn_right(self):
        self.steering = -0.5
    
    def _turn_left(self):
        self.steering = +0.5

    def do_left_turn(self):
        self.turning = [True, False]
        self.old_heading = self.car.heading
        self._turn_left()

    def do_right_turn(self):
        self.turning = [True, False]
        self.old_heading = self.car.heading
        self._turn_right()

    def _turn_0(self):
        self.steering = 0
    
    def accelerate_0(self):
        self.throttle = 0

    def get_next_goal(self):
        return self.path[self.cur_goal]

    def get_position(self):
        return [self.car.center.x, self.car.center.y]

    def get_heading(self): # number 1,2,3,4
        return self.car.heading

    def get_distance(self):
        goal = self.get_next_goal()
        position = self.get_position()
        distance = [goal[0] - position[0], goal[1] - position[1]]
        if abs(distance[0]) < GOAL_RADIUS:
            distance[0] = 0
        if abs(distance[1]) < GOAL_RADIUS:
            distance[1] = 0
        return distance

    def get_best_movement(self):
        # np.mod(, 2*np.pi)
        if self.turning[0]: # turning left
            angle = np.mod(self.old_heading-self.car.heading, 2*np.pi)
            if angle > np.pi:
                angle = (2 * np.pi) - angle
            if angle > np.pi/2:
                self.car.heading = np.mod(self.old_heading + np.pi/2, 2*np.pi)
                self.turning[0] = False
                self._turn_0()
        
        if self.turning[1]: # turning right
            angle = np.mod(self.old_heading-self.car.heading, 2*np.pi)
            if angle > np.pi:
                angle = (2 * np.pi) - angle
            if angle > np.pi/2:
                self.car.heading = np.mod(self.old_heading - np.pi/2, 2*np.pi)
                self.turning[1] = False
                self._turn_0()


        d = self.get_distance()
        if d[0] > d[1]:
            self.accelerate()
        elif d[1] > d[0]:
            self.accelerate()
        else:
            # either turn or we arrived
            self.accelerate()

    def update(self):
        self.get_best_movement()
        self.car.set_control(self.steering, self.throttle)

    def mock_update(self):
        if(self.turning[0] == False):
            self.do_left_turn()
        self.get_best_movement()
        self.car.set_control(self.steering, self.throttle)


## Curvas: o agente a virar para a esquerda andara 5.32 unidades para a frente e 9.32 para a esquerda.
