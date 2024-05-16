from abc import ABC, abstractmethod

class Intersection: #(ABC):        
    
    def __init__(self, index):
        #self.points_dict = {i + 1: tuple(point) for i, point in enumerate(points)}
        #self.limits = {}
        self.cars = []
        self.index = index
        
    def get_point_from_number(self, number):
        if True:# number in self.points_dict:
            return 1 #self.points_dict[number]
        else:
            return None
            
    def __str__(self):
        return str(self.index)

    def add_car(self, car):
        self.cars.append(car)    
    
    def remove_car(self, car):
        self.cars.remove(car)

    def get_number_of_cars(self):
        return len(self.cars)

    def get_number_from_point(self, point):
        pass
    
    def create_limits(self):
        return 1 
        """
        for number, limits in self.limits_dictionary.items():            
            point = self.get_point_from_number(number)
            if point:                
                new_point = (point[0] + limits[0], point[1] + limits[1])
                # Update limits
                self.limits[number] = new_point
        """
    def is_inside_limit(self, point):
        pass
    


    

        


