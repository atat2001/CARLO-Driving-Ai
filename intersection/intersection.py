from abc import ABC, abstractmethod

class Intersection(ABC):        
    
    def __init__(self, points):
        self.points_dict = {i + 1: tuple(point) for i, point in enumerate(points)}
        self.limits = {}
        
    def get_point_from_number(self, number):
        if number in self.points_dict:
            return self.points_dict[number]
        else:
            return None
        
    def get_number_from_point(self, point):
        pass
    
    def create_limits(self):
        for number, limits in self.limits_dictionary.items():            
            point = self.get_point_from_number(number)
            if point:                
                new_point = (point[0] + limits[0], point[1] + limits[1])
                # Update limits
                self.limits[number] = new_point


    def is_inside_limit(self, point):
        pass
    


    

        


