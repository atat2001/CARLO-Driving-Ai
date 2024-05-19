from abc import ABC, abstractmethod

class Intersection: #(ABC):        
    
    def __init__(self, id, roads, phases):
        self.id     = id
        self.roads  = roads
        self.phases = phases        

        self.road_number_dic = {i + 1: road for i, road in enumerate(roads)} 
        self.limits       = {}        
        self.curr_state   = []
        self.cars         = []

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

    def get_relative_position(self, in_road, out_road):                  
        in_number  = self.get_number_from_road(in_road)
        out_number = self.get_number_from_road(out_road)

        if in_number and out_number:
            return (in_number, out_number)
        return None                    
    

    def create_limits(self):
        for number, limits in self.limits_dictionary.items():            
            point = self.get_road_from_number(number)
            if point:                
                new_point = (point[0] + limits[0], point[1] + limits[1])
                # Update limits
                self.limits[number] = new_point


    def is_inside_limit(self, point):
        pass

    def add_car(self, car):
        self.cars.append(car)    
    
    def remove_car(self, car):
        self.cars.remove(car)

    def get_number_of_cars(self):
        return len(self.cars)   

    # def update_phase