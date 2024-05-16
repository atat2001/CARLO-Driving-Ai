
from intersection import Intersection

# So o limits_dictionary é que muda

class Intersection12(Intersection):

    def __init__(self, points):                
        super().__init__(points)
        self.limits_dictionary = {
            1: (0, 10),   
            2: (0, 10),   
            3: (10, 0),   
            4: (10, 0), 
            5: (10, 0),   
            6: (10, 0),   
            7: (0, -10),  
            8: (0, -10),  
            9: (-10, 0),  
            10: (-10, 0)   
        }
        self.create_limits()



        
        
