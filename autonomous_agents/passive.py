from autonomous_agents.autonomous_agents import AutonomousAgent
import numpy as np
from enum import Enum
from geometry import Point  
from shared_variables import dif_via, SIDE_TURN, roads, road_to_intersection, intersections
import time

class Passive(AutonomousAgent):
    def __init__(self, car, path):
        super().__init__(car, path)
        self.skip_until = -1
            
    def try_to_go(self):
        ## rng function here
        if time.time() - self.stop_time > 2:
            self.stop = False
            self.stop_time = 0
            self.skip_until = self.cur_goal
            return True
        return False

        ##### greedy things
    def get_best_movement(self):
        dec = False
        if self.cur_goal != self.skip_until:
            if self.current_intersection != None:
                #print("is it empty?")
                if self.get_next_intersection().get_number_of_cars() > 1:
                    #print("it is")
                    self.stop = True
            if self.stop:
                if(self.car.speed > 0):
                    self.deaccelerate()
                    dec = True
                else:
                    self.car.velocity = Point(0,0)
                    if self.stop_time == 0:
                        self.stop_time = time.time()
                    if not(self.try_to_go()):
                        return 
        
        # np.mod(, 2*np.pi)
        if self.turn_handler(): ## do curva as fast as possible

            if not(dec):
                self.accelerate()
            d = self.get_distance()
            if d[0] == 0 and d[1] == 0: ## se chegou a um ponto
                self.handle_point()
            return
        d = self.get_distance()
        if d[0] == 0 and d[1] == 0: ## se chegou a um ponto
            self.handle_point()  ## handle it
        elif d[0] == 0 or d[1] == 0: ## esta numa reta
            if not(dec):
                self.accelerate()
        else:  ## 
            if not(dec):
                self.accelerate()

    def update(self):
        #print(self.get_next_intersection())
        #print(self.get_current_road())
        if self.car.debug:
            #print(self.car.center)
            print("n:")
            print(self.get_next_goal())
            #print("turning:" + str(self.turning))
            #print("waiting:" + str(self.waiting_for_turn))
        #[print(str(intersections[x]) + "-" + str(intersections[x].get_number_of_cars())) for x in intersections]
        self.update_intersection()
        self.get_best_movement()
        self.car.set_control(self.steering, self.throttle)

    def mock_update(self):
        print(self.get_next_goal())
        self.get_best_movement()
        self.car.set_control(self.steering, self.throttle)