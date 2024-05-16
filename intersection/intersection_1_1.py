
from intersection import Intersection


class Intersection11(Intersection):

    def __init__(self, points):                
        super().__init__(points)
        self.limits_dictionary = {
            1: (0, 10),   
            2: (0, 10),   
            3: (10, 0),   
            4: (10, 0),   
            5: (0, -10),  
            6: (0, -10),  
            7: (-10, 0),  
            8: (-10, 0)   
        }
        self.create_limits()
        
        
