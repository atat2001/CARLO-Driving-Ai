from autonomous_agents.autonomous_agents import AutonomousAgent


class PhaseAgent(AutonomousAgent):
    def __init__(self, car, path):
        super().__init__(car, path)

    def update(self):
        pass

    def get_best_movement(self):
        pass

    def is_agent_in_curr_phase(self):
        relative_pos_to_int = self.current_intersection.get_relative_position(self.car.center)
        curr_phase = self.calculate_curr_phase()

        if relative_pos_to_int in curr_phase:
            return True
        return False
    
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