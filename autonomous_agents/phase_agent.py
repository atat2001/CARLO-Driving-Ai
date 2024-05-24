from autonomous_agents.autonomous_agents import AutonomousAgent
from geometry import Point


class PhaseAgent(AutonomousAgent):
    def __init__(self, car, path, id=0):
        super().__init__(car, path)
        self.id = id
        self.color = "green"
        self.car.color = self.color
        self.last_decision = -1
        self.stopping = False

    def is_agent_in_curr_phase(self):

        if self.current_intersection == None:
            return True

        relative_pos_to_int = self.current_intersection.get_relative_position(
            self.get_current_road(), self.get_next_road()
        )
        curr_phase = self.calculate_curr_phase()

        if curr_phase == None:
            return True

        if relative_pos_to_int and relative_pos_to_int in curr_phase:
            return True
        return False

    def calculate_curr_phase(self):
        phases = self.current_intersection.get_phases()
        state = self.current_intersection.get_state()

        if len(phases) == 0:
            return None  # not an intersection

        phase_voting = {}

        for index, phase in phases.items():
            for busy_point in state:
                if busy_point in phase:
                    if index in phase_voting.keys():
                        phase_voting[index] += 1
                    else:
                        phase_voting[index] = 1

        if len(phase_voting) == 0:
            return 1  # default phase if no cars in intersection

        chosen_phase = max(phase_voting, key=phase_voting.get)

        return phases[chosen_phase]

    def make_decision(self):
        if self.cur_goal % 2 == 0 or self.cur_goal < self.last_decision + 2:
            return

        self.last_decision = self.cur_goal

        if self.current_intersection != None:
            if not self.is_agent_in_curr_phase():
                self.stopping = True
                self.decision = False
            else:
                self.set_decision(True)
                #self.decision = True

    def apply_decision(self):
        if self.decision:  ## se a decisao for positiva vai
            self.accelerate()
        elif (
            self.stopping
        ):  ## se a decisao for negativa e estiver a parar continua a parar
            self.stop_car()
        else:  # se a decisao for negativa mas nao tiver mais a parar compara os timers:
            b = False
            if self.cur_goal % 2 == 0:
                b = True
                self.cur_goal -= 1
            if self.is_agent_in_curr_phase():
                self.decision = True
                #self.in_decision = False
                #self.update_intersection()
                self.accelerate()
            else:
                self.accelerate_0()
            if b:
                self.cur_goal += 1

    def update(self):
        self.get_best_movement()  ## used to update point, intersection and steering
        if self.cur_goal % 2 == 1:
            self.update_intersection()
        if self.in_decision or self.is_decision_time():
            self.in_decision = True
            self.accelerate_0()  ## steering
            self.make_decision()
            self.apply_decision()
        self.stop_for_car_in_front()
        self.car.set_control(self.steering, self.throttle)

    def get_best_movement(self):
        if self.turn_handler():  ## do curva as fast as possible
            self.accelerate()
            d = self.get_distance()
            if d[0] == 0 and d[1] == 0:  ## se chegou a um ponto
                self.handle_point()
            return
        d = self.get_distance()
        if d[0] == 0 and d[1] == 0:  ## se chegou a um ponto
            self.handle_point()  ## handle it
        elif d[0] == 0 or d[1] == 0:  ## esta numa reta
            self.accelerate()
        else:
            self.accelerate()

    def stop_car(self):  # redundant function from passive.py
        if self.car.speed > 0:
            self.deaccelerate()
        else:
            self.car.velocity = Point(0, 0)
            self.stopping = False
