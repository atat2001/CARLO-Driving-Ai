from autonomous_agents.autonomous_agents import AutonomousAgent
from geometry import Point  
import time
import random

class Passive(AutonomousAgent):
    
    def __init__(self, car, path, id = 0):
        super().__init__(car, path)
        self.stop_time = 0
        self.last_decision = -1
        self.stopping = False
        self.id = id
        self.rng = 0

    def try_to_go(self):
        ## rng function here
        return time.time() - self.stop_time > self.rng

        ##### greedy things
    def get_best_movement(self):
        if self.cur_goal % 2 == 0:
            self.update_intersection()
        if self.turn_handler(): ## do curva as fast as possible
            self.accelerate()
            d = self.get_distance()
            if d[0] == 0 and d[1] == 0: ## se chegou a um ponto
                self.handle_point()
            return
        d = self.get_distance()
        if d[0] == 0 and d[1] == 0: ## se chegou a um ponto
            self.handle_point()  ## handle it
        elif d[0] == 0 or d[1] == 0: ## esta numa reta
            self.accelerate()
        else:  ## 
            self.accelerate()

    def update_decision(self):
        if self.cur_goal == self.last_decision or (self.cur_goal%2 == 0 and self.last_decision == self.cur_goal-1):  ## only do decision once, on first point
            return
        
        if(self.id > 10):
            print("decision")
            print(self.current_intersection)
            print(self.get_next_intersection())
            print(self.current_intersection.get_number_of_cars())
        self.last_decision = self.cur_goal

        if self.current_intersection != None:
            if self.current_intersection.get_number_of_cars() > 1:
                print(f"{self.id}: stopping")
                self.stopping = True
                self.decision = False
                return
            else:
                print(f"{self.id}: going")
                self.decision = True

    def stop_car(self):
        if(self.car.speed > 0):
            self.deaccelerate()
        else:
            self.car.velocity = Point(0,0)
            self.stop_time = time.time()
            self.rng = 1 + random.randint(1, 20)/10
            self.stopping = False
    

    def apply_decision(self):
        if self.decision:  ## se a decisao for positiva vai
            self.accelerate()
        elif self.stopping:   ## se a decisao for negativa e estiver a parar continua a parar
            self.stop_car()
        else: # se a decisao for negativa mas nao tiver mais a parar compara os timers:
            if self.try_to_go():
                self.decision = True
                self.in_decision = False
                self.update_intersection() # due to a bug keep this here
                self.accelerate()
            else:
                self.accelerate_0()

    def update(self):
        #print(self.get_next_intersection())
        #print(self.get_current_road())
        if self.car.debug:
            #print(self.car.center)
            print(f"{self.id}: n:")
            print(self.get_next_goal())
            #print(f"{self.id}: turning:" + str(self.turning))
            #print(f"{self.id}: waiting:" + str(self.waiting_for_turn))
        #[print(str(intersections[x]) + "-" + str(intersections[x].get_number_of_cars())) for x in intersections]
        self.update_intersection()
        if(self.is_decision_time() or self.in_decision):
            self.in_decision = True
            self.get_best_movement()
            self.accelerate_0()
            self.update_decision()
            self.apply_decision()
            #self.update_intersection()  ## nao sei, se mudo a ordem da um bug, ao contrario da outro...
        else:
            self.get_best_movement()
        self.car.set_control(self.steering, self.throttle)

    def mock_update(self):
        print(self.get_next_goal())
        self.get_best_movement()
        self.car.set_control(self.steering, self.throttle)