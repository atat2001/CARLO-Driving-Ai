import numpy as np
from enum import Enum
from geometry import Point  
from shared_variables import dif_via, SIDE_TURN, roads, road_to_intersection, intersections

import time

GOAL_RADIUS = 2
TURN_FRONT = 5.36
INTERSECTION_DISTANCE = 400  ## distance to the intersection to start slowing down (consider it squared so 400=20)

class AutonomousAgent:
    def __init__(self, car, path):
        self.roads = path
        self.path = [[car.center.x, car.center.y]] + self.create_path(path)
        self.cur_goal = 1
        self.car = car
        self.car.debug = False
        self._steering = 0
        self._throttle = 0
        self.turning = [False, False]
        self.old_heading = None
        self.waiting_for_turn = [False, False]
        self.current_intersection = None
        self.stop = False
        self.stop_time = 0

    def update_intersection(self): 
        if self.current_intersection != None:# esta na intercecao
            if self.get_next_intersection() != self.current_intersection: # verifica se ja acabou a intercecao
                self.current_intersection.remove_car(self.car)
                self.current_intersection = None
        else:   # nao esta na intercecao
            road_id = self.get_current_road()
            if self.get_next_goal() == roads[road_id][1]:  ## se o proximo goal for o inicio de uma intercecao
                dist = self.get_distance()
                dist = dist[0]*dist[0] + dist[1]*dist[1]
                if dist < INTERSECTION_DISTANCE:
                    self.current_intersection = self.get_next_intersection()
                    self.current_intersection.add_car(self.car)

    def get_current_road(self):
        return self.roads[self.cur_goal // 2]

    def get_next_intersection(self):
        return intersections[road_to_intersection[self.get_current_road()]]

    @property
    def steering(self):
        return self._steering
    @property
    def throttle(self):
        #print("going vruuum")
        return self._throttle

    def create_path(self, path):
        returner = [roads[path[0]][1]]
        for i in path[1:]:
            returner += roads[i]
        return returner

    @steering.setter
    def steering(self, val):
        self._steering = val
        
    @throttle.setter
    def throttle(self, val):
        #print(self._throttle)
        self._throttle = val

    def accelerate(self):
        #print("vrum vrum")
        self.throttle = 1.5

    def deaccelerate(self):
        self.throttle = -1.5

    def wait_for_right_moment(self):
        last_dir = self.get_last_direction(1)
        d = self.get_distance()
        if last_dir[0] == 0:
            return abs(d[1]) < TURN_FRONT
        elif last_dir[1] == 0:
            return abs(d[0]) < TURN_FRONT
        return False

    def _turn_right(self):
        self.steering = -0.5
    
    def _turn_left(self):
        self.steering = +0.5

    def do_left_turn(self):
        self.turning = [True, False]
        self.old_heading = self.car.heading
        self._turn_left()


    def do_right_turn(self):
        self.turning = [False, True]
        self.old_heading = self.car.heading
        self._turn_right()

    def prepare_right_turn(self):
        self.waiting_for_turn = [False, True]
        if not(self.wait_for_right_moment()):
            return
        else:
            self.waiting_for_turn = [False, False]
            self.do_right_turn()

    def prepare_left_turn(self):
        self.waiting_for_turn = [True, False]
        if not(self.wait_for_right_moment()):
            return
        else:
            self.waiting_for_turn = [False, False]
            self.do_left_turn()

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

    def get_last_direction(self, i = 0):
        return [self.path[self.cur_goal-i][0] - self.path[self.cur_goal-1-i][0], self.path[self.cur_goal-i][1] - self.path[self.cur_goal-1-i][1]]

    def increment_cur_goal(self):
        if self.cur_goal != len(self.path)-1:
            self.cur_goal += 1
        else:
            self.car.movable = False

    def get_distance(self):
        goal = self.get_next_goal()
        position = self.get_position()
        distance = [goal[0] - position[0], goal[1] - position[1]]
        if abs(distance[0]) < GOAL_RADIUS:
            distance[0] = 0
        if abs(distance[1]) < GOAL_RADIUS:
            distance[1] = 0
        return distance

    def turn_handler(self):
        #print(self.waiting_for_turn)
        if self.waiting_for_turn[0]:
            self.prepare_left_turn()
        if self.waiting_for_turn[1]:
            self.prepare_right_turn()

        if self.turning[0]: # turning left
            angle = np.mod(self.old_heading-self.car.heading, 2*np.pi)
            if angle > np.pi:
                angle = (2 * np.pi) - angle
            if angle > np.pi/2:
                self.car.heading = np.mod(self.old_heading + np.pi/2, 2*np.pi)
                self.turning[0] = False
                self._turn_0()
                if self.car.heading == np.pi or self.car.heading == 0:
                    self.car.center = Point(self.car.center.x,self.get_next_goal()[1])
                else:
                    self.car.center = Point(self.get_next_goal()[0],self.car.center.y)
        if self.turning[1]: # turning right
            angle = np.mod(self.old_heading-self.car.heading, 2*np.pi)
            if angle > np.pi:
                angle = (2 * np.pi) - angle
            if angle > np.pi/2:
                self.car.heading = self.old_heading - np.pi/2
                if self.car.heading < 0:
                    self.car.heading+= 2*np.pi
                self.turning[1] = False
                self._turn_0()
                if self.car.heading == np.pi or self.car.heading == 0:
                    self.car.center = Point(self.car.center.x,self.get_next_goal()[1])
                else:
                    self.car.center = Point(self.get_next_goal()[0],self.car.center.y)

        return self.turning[0] or self.turning[1] ## did it do something?

    def handle_point(self):
        if self.car.debug:
            print("handling thing")
        last_dir = self.get_last_direction()
        self.increment_cur_goal()
        new_dir = self.get_last_direction()
        if last_dir[0] == 0:  ## se antes de chegar ao ponto estiver a ir reto na vertical
            if last_dir[1] > 0: ## se estiver a ir para cima
                if new_dir[0] > 0: ## virar a direita
                    self.prepare_right_turn()
                elif new_dir[0] < 0:
                    self.prepare_left_turn()
            else: # esta a ir para baixo
                if new_dir[0] > 0: ## virar a esquerda
                    self.prepare_left_turn()
                elif new_dir[0] < 0:
                    self.prepare_right_turn()
        elif last_dir[1] == 0:  ## se antes de chegar ao ponto estiver a ir reto na horizontal
            if last_dir[0] > 0: ## se estiver a ir para a direita
                if new_dir[1] > 0: ## virar a esquerda
                    self.prepare_left_turn()
                elif new_dir[1] < 0:
                    self.prepare_right_turn()
            else:  ## se estiver a ir para a esquerda
                if new_dir[1] > 0: ## virar a direita
                    self.prepare_right_turn()
                elif new_dir[1] < 0:
                    self.prepare_left_turn()

    def get_best_movement(self):
        print("Autonomous_agent: get_best_movement not implemented for this class")

    def update(self):
        print("Autonomous_agent: update not implemented for this class")


