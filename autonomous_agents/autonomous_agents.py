import numpy as np
from geometry import Point  
from shared_variables import dif_via, SIDE_TURN, roads, road_to_intersection, intersections, INTERSECTION_DISTANCE, THROTTLE, TIMESTEP,roads_to_cars
from enum import Enum
import time
import math

GOAL_RADIUS = 2
TURN_FRONT = 5.36
TURN_THRESHOLD = 1   ## used to fix a small bug
INTERSECTION_DISTANCE = 400  ## distance to the intersection to start slowing down (consider it squared so 400=20)

class AutonomousAgent:
    def __init__(self, car, path):
        self.roads = path
        self.car = car
        self.init_car()

        self.path = [[car.center.x, car.center.y]] + self.create_path(path)
        self.cur_goal = 1
        #self.car.debug = False
        self._steering = 0
        self._throttle = 0
        self.turning = [False, False]
        self.old_heading = None
        self.waiting_for_turn = [False, False]
        self.current_intersection = None
        self.stop = False
        self.decision = False
        self.in_decision = False
        #roads_to_cars[self.get_current_road()] = roads_to_cars.get(self.get_current_road(),[]) + [self.car]

    def set_decision(self,b):
        if b == True:
            self.car.passed_objective = True
        self.decision = b

    def update_current_road(self):
        ## do once cur_objective % 2 == 0
        if self.cur_goal % 2 == 1:
            roads_to_cars[self.roads[(self.cur_goal-2)// 2]] = [car for car in roads_to_cars.get(self.roads[(self.cur_goal-2)// 2],[]) if car != self.car]
            roads_to_cars[self.get_current_road()] = roads_to_cars.get(self.get_current_road(),[]) + [self.car]
            self.car.passed_objective = False
        else:
            self.car.passed_objective = self.decision

    def get_cars_in_road(self):
        if self.cur_goal % 2 == 0:
            return []
        return roads_to_cars.get(self.get_current_road(), [])

    def get_car_in_front(self):
        if self.car.movable == False:
            return None
        cars = self.get_cars_in_road()
        if len(cars) == 0:
            return None
        last_point = self.get_next_goal()
        cur_point = self.get_position()
        diff = [last_point[0] - cur_point[0], last_point[1] - cur_point[1]]
        diff_norm = diff[0]*diff[0]+diff[1]+diff[1]
        smallest_bigger_car = None
        smallest_bigger_car_diff_norm = None
        for car in self.get_cars_in_road():
            if car.movable == False:
                continue
            car_diff = [last_point[0] - car.center.x, last_point[1] - car.center.y]
            car_diff_norm = car_diff[0]*car_diff[0]+car_diff[1]+car_diff[1]
            if car.passed_objective:
                car_diff_norm = 0 
            if car_diff_norm < diff_norm and (smallest_bigger_car_diff_norm == None or car_diff_norm > smallest_bigger_car_diff_norm):
                smallest_bigger_car_diff_norm = car_diff_norm
                smallest_bigger_car = car
        if smallest_bigger_car == None:
            return None
        print("returning car\n")
        return smallest_bigger_car

    def stop_for_car_in_front(self):
        aux = self.get_car_in_front()
        if aux != None:
            if aux.passed_objective:
                last_point = self.get_next_goal()
                cur_point = self.get_position()
                dist = abs(last_point[0] - cur_point[0] + last_point[1] - cur_point[1])
            else:
                dist = abs(self.car.center.x - aux.center.x + self.car.center.y - aux.center.y)
            ## estamos a assumir que estao em linha reta, ou seja um vai estar a 0
            print(f"distance is: {dist}")
            print(f"from: {self.car.color} to: {aux.color}")
            min_distance = self.get_brake_distance() + 5
            print(f"min_dist is {min_distance}\n\n")
            #if self.car.color == "yellow":
                #exit()
            if(dist < min_distance):
                print("breaking \n\n")
                self.deaccelerate()

################################################################################################################################################
################################################################################################################################################
    def init_car(self):
        car = self.car
        car.center = Point((roads[self.roads[0]][0][0] + roads[self.roads[0]][1][0])/2, (roads[self.roads[0]][1][1] + roads[self.roads[0]][0][1])/2)
        if(roads[self.roads[0]][1][0] - roads[self.roads[0]][0][0] == 0):
            car.heading = 3*np.pi/2
            if(roads[self.roads[0]][1][1] - roads[self.roads[0]][0][1] > 0):
                car.heading = np.pi/2
        elif(roads[self.roads[0]][1][1] - roads[self.roads[0]][0][1] == 0):
            car.heading = 0
            if(roads[self.roads[0]][1][0] - roads[self.roads[0]][0][0] < 0):
                car.heading = np.pi

    def update_intersection(self):    # adiciona o carro a intercecao
        if self.current_intersection != None:# esta na intercecao
            #print("esta na intercecao")
            if self.get_next_intersection() != self.current_intersection and not self.in_decision: # verifica se ja acabou a intercecao e se ja acabou a decisao
                #print("changed intersection")
                self.remove_intersection_data()
                self.current_intersection = None
        if self.current_intersection == None:   # nao esta na intercecao
            #print("nao esta na intercecao")
            road_id = self.get_current_road()
            if self.get_next_goal() == roads[road_id][1]:  # se o proximo goal for o inicio de uma intersection
                dist = self.get_distance()
                dist = dist[0]*dist[0] + dist[1]*dist[1]
                if dist < INTERSECTION_DISTANCE:
                    print("added to intersection")
                    self.current_intersection = self.get_next_intersection() 
                    self.add_intersection_data() 
        #   print("}")

    def get_brake_distance(self):
        cur_speed = self.car.speed
        time_breaking = cur_speed/THROTTLE + 2*TIMESTEP
        return max(cur_speed*time_breaking - 0.5*THROTTLE*time_breaking*time_breaking,0) # o copilot escreveu isto e estava certo :O
        
            
    def is_decision_time(self):
        if self.cur_goal % 2 == 0:
            return False
        if self.current_intersection != None: ## 
            dist = self.get_distance()
            dist_to_intersection = math.sqrt(dist[0]*dist[0] + dist[1]*dist[1])

            if self.get_brake_distance() >= dist_to_intersection:  ## MAKE DECISION
                print("is_decision_time " + str(self.id))
                return True
        return False

    def get_current_road(self):
        return self.roads[self.cur_goal // 2]
    
    def get_next_road(self):
        if (self.cur_goal + 2) // 2 < len(self.roads):
            return self.roads[(self.cur_goal + 2) // 2]
        else:
            return None

    def get_next_intersection(self):
        return intersections[road_to_intersection[self.get_current_road()]]
    
    def add_intersection_data(self):                        
        # Add car and Current State 
        self.current_intersection.add_car(self.car, self.get_current_road())                                        

        if self.cur_goal + 1 < len(self.path): #ha paths que acaba no inicio de uma intersection, entao da erro                                               
            curr_road = self.get_current_road()
            next_road = self.get_next_road()
            self.curr_state = (curr_road, next_road) 
            self.current_intersection.add_state(curr_road, next_road) 
    
    def remove_intersection_data(self):
        self.current_intersection.remove_car(self.car)                                
        self.current_intersection.remove_state(self.curr_state[0], self.curr_state[1]) #eliminar acao feita                
        self.current_intersection = None


    def different_get_current_intersection(self):
        return intersections[road_to_intersection[self.roads[self.cur_goal-1 // 2]]]

    @property
    def steering(self):
        return self._steering
    @property
    def throttle(self):        
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
        self._throttle = val

    def accelerate(self):
        #print("vrum vrum")
        self.throttle = THROTTLE

    def deaccelerate(self):
        self.throttle = -1*THROTTLE

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
        x = self.path[self.cur_goal-i][0] - self.path[self.cur_goal-1-i][0]
        y = self.path[self.cur_goal-i][1] - self.path[self.cur_goal-1-i][1]
        if abs(x) < TURN_THRESHOLD:
            x = 0
        if abs(y) < TURN_THRESHOLD:
            y = 0
        return [x, y]

    def increment_cur_goal(self):
        #print(f"incrementing-----------------------------------{self.cur_goal-(-1)}")
        
        if self.cur_goal != len(self.path)-1:
            #print("success")
            self.cur_goal += 1
            #if self.cur_goal % 2 == 0:
            #    self.update_intersection()
        else:
            if self.current_intersection != None:
                try:
                    self.remove_intersection_data()
                except:
                    pass
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
        #print("handling thing")
        if self.car.debug:
            #print("handling thing")
            pass
        last_dir = self.get_last_direction()
        prev_goal = self.get_next_goal()
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

        if self.car.heading == np.pi or self.car.heading == 0:
            self.car.center = Point(self.car.center.x,prev_goal[1])
        else:
            self.car.center = Point(prev_goal[0],self.car.center.y)

        if self.cur_goal % 2 == 1: 
            self.in_decision = False
            self.update_intersection()
        self.update_current_road()

    def get_best_movement(self):
        print("AutonomousAgent: get_best_movement not implemented for this class")

    def update(self):
        print("AutonomousAgent: update not implemented for this class")


