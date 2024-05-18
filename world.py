from agents import Car, Pedestrian, RectangleBuilding
from entities import Entity
from typing import Union
from visualizer import Visualizer
from enum import Enum
import time
from shared_variables import intersections, intersection_roads
from intersection.intersection import Intersection

class World:
    def __init__(self, dt: float, width: float, height: float, ppm: float = 8):
        self.dynamic_agents = []
        self.static_agents  = []
        self.t  = 0  # simulation time
        self.dt = dt # simulation time step
        self.visualizer = Visualizer(width, height, ppm=ppm)
        self.last_tick_time = time.time()
                        
        self.initialize_intersections()
                

    @property
    def agents(self):
        return self.static_agents + self.dynamic_agents
        
    def add(self, entity: Entity):
        if entity.movable:
            self.dynamic_agents.append(entity)
        else:
            self.static_agents.append(entity)
        
    def tick(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_tick_time
        self.last_tick_time = current_time
        for agent in self.dynamic_agents:
            agent.tick(self.dt * (elapsed_time))
        self.t += self.dt
    
    def render(self):
        self.visualizer.create_window(bg_color = 'gray')
        self.visualizer.update_agents(self.agents)        
    
    def initialize_intersections(self):       
        #Atualiza as intersections do shared_variables e depois os agentes acedem a isso      
        for id, roads in intersection_roads.items():
            phases = [] #TO-DO 
            intersections[id] = Intersection(id, roads, phases)        
        
    def collision_exists(self, agent = None):
        if agent is None:
            for i in range(len(self.dynamic_agents)):
                for j in range(i+1, len(self.dynamic_agents)):
                    if self.dynamic_agents[i].collidable and self.dynamic_agents[j].collidable:
                        if self.dynamic_agents[i].collidesWith(self.dynamic_agents[j]):
                            return True
                for j in range(len(self.static_agents)):
                    if self.dynamic_agents[i].collidable and self.static_agents[j].collidable:
                        if self.dynamic_agents[i].collidesWith(self.static_agents[j]):
                            return True
            return False
            
        if not agent.collidable: return False
        
        for i in range(len(self.agents)):
            if self.agents[i] is not agent and self.agents[i].collidable and agent.collidesWith(self.agents[i]):
                return True
        return False
    
    def get_collisions(self):
        collisions = []
        for i in range(len(self.dynamic_agents)):
            for j in range(i+1, len(self.dynamic_agents)):
                if self.dynamic_agents[i].collidable and self.dynamic_agents[j].collidable:
                    if self.dynamic_agents[i].collidesWith(self.dynamic_agents[j]):
                        collisions.append((self.dynamic_agents[i], self.dynamic_agents[j]))
            for j in range(len(self.static_agents)):
                if self.dynamic_agents[i].collidable and self.static_agents[j].collidable:
                    if self.dynamic_agents[i].collidesWith(self.static_agents[j]):
                        collisions.append((self.dynamic_agents[i], self.static_agents[j]))
        return collisions
    
    def close(self):
        self.reset()
        self.static_agents = []
        if self.visualizer.window_created:
            self.visualizer.close()
        
    def reset(self):
        self.dynamic_agents = []
        self.t = 0

'''
class TypeObj(Enum):
    LANE_START = 0
    INTERSECTION_START = 1
    INTERSECTION_DECISION = 2
    INTERSECTION_END = 3

class Objective:
    def __init__(self, position, heading, type_obj, intersection):
        self.position = position
        self.heading = heading
        self.type_obj = type_obj
        self.intersection = intersection

class lane:
    def __init__(self, lane_start, intersection_start, decision, end):
        self.lane_start = lane_start
        self.intersection_start = intersection_start
        self.decision = decision
        self.end = end

class intersection:
    def __init__(self, lanes, phases):
        self.lanes = lanes
        self.phases = phases
        self.move_to_phases = dict() # todo
        self.cars = []
    
    def add_car(self, car):
        self.cars += [car]
        self.increment_phases(car)

    def remove_car(self, car):
        # todo
        if(self.phases.get(car.get_phase(), None) != None):
            for phase in self.move_to_phases[car.get_target_lane()]:
                phase += 1

    def get_max_phase(self):
        # todo
        return 
        #for phase in self.phases:

    def increment_phases(self, car):
        # todo
        if(phases.get(car.get_phase(), None) != None):
            for phase in self.move_to_phases[car.get_target_lane()]:
                phase += 1
                
'''           
        
