from autonomous_agents.autonomous_agents import AutonomousAgent
from geometry import Point


class PhaseAgent(AutonomousAgent):
    def __init__(self, car, path):
        super().__init__(car, path)
        self.last_decision = -1

    def is_agent_in_curr_phase(self):
        relative_pos_to_int = self.current_intersection.get_relative_position(self.get_current_road(), self.get_next_road())
    
    def calculate_curr_phase(self):
        phases = self.current_intersection.get_phases()
        state = self.current_intersection.get_state()

        if (len(phases) == 0):
            return None # not an intersection

        phase_voting = {}

        for index, phase in phases.items():
            for busy_point in state:
                if busy_point in phase:
                    if index in phase_voting.keys():
                        phase_voting[index] += 1
                    else:
                        phase_voting[index] = 1

        if len(phase_voting) == 0: 
            return 1 # default phase if no cars in intersection
        
        chosen_phase = max(phase_voting, key=phase_voting.get)

        return phases[chosen_phase]
    
    def update_decision(self):
        if self.cur_goal == self.last_decision or (self.cur_goal%2 == 0 and self.last_decision == self.cur_goal-1):  ## only do decision once, on first point
            return
        
        self.last_decision = self.cur_goal

        if self.current_intersection != None:
            if not self.is_agent_in_curr_phase():
                self.stopping = True
                self.decision = False
                return
            else:
                self.decision = True

    def apply_decision(self):
        if self.decision:  ## se a decisao for positiva vai
            self.accelerate()
        elif self.stopping:   ## se a decisao for negativa e estiver a parar continua a parar
            self.stop_car()
        else: # se a decisao for negativa mas nao tiver mais a parar compara os timers:
            
            if self.is_agent_in_curr_phase():
                self.decision = True
                self.in_decision = False
                self.update_intersection() # due to a bug keep this here
                self.accelerate()
            else:
                self.accelerate_0()
    
    def update(self):
        self.update_intersection()
        if (self.is_decision_time() or self.in_decision):
            self.in_decision = True
            self.get_best_movement()
            self.accelerate_0()
            self.update_decision()
            self.apply_decision()
        else:
            self.get_best_movement()
        self.car.set_control(self.steering, self.throttle)

    def get_best_movement(self): # redundant function from greedy.py and passive.py
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
        else:
            self.accelerate()
    
    def stop_car(self): # redundant function from passive.py
        if(self.car.speed > 0):
            self.deaccelerate()
        else:
            self.car.velocity = Point(0,0)
            self.stopping = False