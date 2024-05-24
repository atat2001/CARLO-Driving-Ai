
class Intersection:  
    
    def __init__(self, id, roads, phases):
        self.id     = id
        self.roads  = roads
        self.phases = phases        

        self.road_number_dic = {i + 1: road for i, road in enumerate(roads)}           
        self.curr_state   = []
        self.cars         = []
        self.car_to_road  = {}


    def __str__(self):
        return f"Intersection {self.id}"


    def get_road_from_number(self, number):
        if number in self.road_number_dic:
            return self.road_number_dic[number]
        else:
            return None


    def get_number_from_road(self, road):
        for number, road_ in self.road_number_dic.items():
            if road == road_:
                return number
        return None
    

    def add_state(self, in_road, out_road):
        state = self.get_relative_position(in_road, out_road)      

        if state:
            self.curr_state.append(state)                


    def remove_state(self, in_road, out_road):                
        if in_road and out_road:
            in_number  = self.get_number_from_road(in_road)
            out_number = self.get_number_from_road(out_road)
            state = (in_number, out_number)            

            if state in self.curr_state:
                self.curr_state.remove(state)

    def get_state(self):
        return self.curr_state

    def get_phases(self):
        return self.phases
    
    def get_cars(self):
        return self.cars

    def get_relative_position(self, in_road, out_road):                  
        in_number  = self.get_number_from_road(in_road)
        out_number = self.get_number_from_road(out_road)

        if in_number and out_number:
            return (in_number, out_number)
        return None                    

    def add_car(self, car, road):
        print("adding car")
        self.cars.append(car)
        self.car_to_road[car] = road    
    
    def remove_car(self, car):
        print("removing car")
        self.cars.remove(car)
        del self.car_to_road[car]

    def get_number_of_cars(self):
        return len(self.cars)   

    def get_priority_nr(self,car):
        ## pega na road atual(se entrar numa intercessao pega na road anterior)
        return self.roads.index(self.car_to_road[car])

    def has_priority(self,autonomous_agent):
        if not(autonomous_agent.car.movable):
            return True
        for car in self.cars:
            if self.get_priority_nr(car) < self.get_priority_nr(autonomous_agent.car):
                return False
        return True
    