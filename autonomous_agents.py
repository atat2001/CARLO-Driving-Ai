import numpy as np
LANE_DISTANCE = 5
GOAL_RADIUS = 2
SIDE_TURN = np.pi/15
class Greedy:
    def __init__(self, car, path):
        self.path = path
        self.cur_goal = 0
        self.car = car
        self._steering = 0
        self._throttle = 0

    @property
    def steering(self):
        return self._steering
    @property
    def throttle(self):
        print("going vruuum")
        return self._throttle

    @steering.setter
    def steering(self, val):
        self._steering = val
    @throttle.setter
    def throttle(self, val):
        print(self._throttle)
        self._throttle = val

    def accelerate(self):
        print("vrum vrum")
        self.throttle = 1.5

    def deaccelerate(self):
        self.throttle = -1.5

    def turn_right(self):
        self.steering = -0.5
    
    def turn_left(self):
        self.steering = +0.5

    def turn_0(self):
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
