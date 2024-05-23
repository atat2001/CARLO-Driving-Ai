from autonomous_agents.autonomous_agents import AutonomousAgent

class Greedy(AutonomousAgent):
    def __init__(self, car, path, id):
        self.id = id
        super().__init__(car, path)
        self.car.color = 'red'

    ##### greedy things
    def get_best_movement(self):
        # np.mod(, 2*np.pi)
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

    def update(self):
        self.decision = True
        #print(self.get_next_intersection())
        #print(self.get_current_road())
        if self.car.debug:
            print(self.car.center)
            print(self.get_next_goal())
            print("turning:" + str(self.turning))
            print("waiting:" + str(self.waiting_for_turn))
        #[print(str(intersections[x]) + "-" + str(intersections[x].get_number_of_cars())) for x in intersections]
        self.get_best_movement()
        if self.cur_goal % 2 == 1:
            self.update_intersection()
        self.stop_for_car_in_front()
        print(self.throttle)
        self.car.set_control(self.steering, self.throttle)



## Curvas: o agente a virar para a esquerda andara 5.32 unidades para a frente e 9.32 para a esquerda.
