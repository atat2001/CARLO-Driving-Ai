from autonomous_agents.autonomous_agents import AutonomousAgent
from geometry import Point  
import time
import random

class Social(AutonomousAgent):
    
    def __init__(self, car, path, id = 0):
        super().__init__(car, path)
        self.stop_time = 0
        self.last_decision = -1
        self.stopping = False
        self.id = id
        self.order = -1

    def try_to_go(self):
        ## rng function here
        return self.current_intersection.has_priority(self)

        ##### greedy things
    def get_best_movement(self):
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
        else:
            self.accelerate()

    def make_decision(self):
        if self.cur_goal % 2 == 0 or self.cur_goal < self.last_decision+2:  ## only do decision once, on first point
            return

        self.last_decision = self.cur_goal
        print("making decision")
        if self.current_intersection != None:
            if not(self.current_intersection.has_priority(self)):
                print(f"{self.id}: stopping")
                self.stopping = True    # define que o carro vai ter de parar asap
                self.decision = False
                return
            else:
                print(f"{self.id}: going")
                self.set_decision(True)
                #self.decision = True

    def stop_car(self):
        if(self.car.speed > 0):
            self.deaccelerate()
        else:
            self.car.velocity = Point(0,0)
            self.stop_time = time.time()
            self.rng = 1 + random.randint(1, 20)/10 # not used here right?
            self.stopping = False
    
    def apply_decision(self):
        if self.decision:  ## se a decisao for positiva vai
            self.accelerate()
        elif self.stopping:   ## se a decisao for negativa e estiver a parar continua a parar
            self.stop_car()
        else: # se a decisao for negativa mas nao tiver mais a parar compara os timers:
            if self.try_to_go():
                self.set_decision(True)
                #self.decision = True
                self.in_decision = False
                self.update_intersection() # due to a bug keep this here
                self.accelerate()
            else:
                self.accelerate_0()

    def update(self):
        self.get_best_movement()  ## used to update point, intersection and steering
        
        if self.cur_goal % 2 == 1: 
            self.update_intersection()
        if(self.in_decision or self.is_decision_time()):
            self.in_decision = True
            self.accelerate_0()       ## steering
            self.make_decision()
            self.apply_decision()
            #self.update_intersection()  ## nao sei, se mudo a ordem da um bug, ao contrario da outro...
        self.car.set_control(self.steering, self.throttle)
