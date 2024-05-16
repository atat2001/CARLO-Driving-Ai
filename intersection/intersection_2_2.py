
from intersection import Intersection


class Intersection22(Intersection):

    def __init__(self, points):                
        super().__init__(points)
        self.limits_dictionary = {
            1: (0, 10),   2: (0, 10),   3: (0, 10),   4: (0, 10),   
            5: (10, 0),   6: (10, 0),   7: (10, 0),   8: (10, 0),   
            9: (0, -10),  10: (0, -10), 11: (0, -10), 12: (0, -10),  
            13: (-10, 0), 14: (-10, 0), 15: (-10, 0), 16: (-10, 0)   
        }
        self.create_limits()
        
