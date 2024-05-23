from entities import Entity
from visualizer import Visualizer
import time
from shared_variables import intersections, intersection_roads, intersection_phases, roads_to_cars, TIMESTEP
from intersection.intersection import Intersection

DEBUG_ROAD_LINES = True # used to debug road lines
TIME = 30               # time in seconds

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
        for id, roads in intersection_roads.items():
            intersections[id] = Intersection(id, roads, intersection_phases[id])    
    
    # Deixo estes dois metodos no world?
    def remove_car(self, car):
        for road, cars in roads_to_cars.items():
            if car in cars:
                cars.remove(car)
                break

    def remove_car_from_intersections(self, car): #Nome???
        for intersection in intersections.values():
            if car in intersection.cars:
                intersection.remove_car(car)

    def delete_dynamic_agent(self, agent):
        self.remove_car(agent)        
        self.remove_car_from_intersections(agent)
        self.dynamic_agents.remove(agent)

    def find_agent_by_car(self, car, autonomous_agents):
        for agent in autonomous_agents:
            if agent.car == car:
                return agent
        return None

    def collision_exists(self, agents, agent = None):
        if agent is None:
            for i in range(len(self.dynamic_agents)):
                for j in range(i+1, len(self.dynamic_agents)):
                    if self.dynamic_agents[i].collidable and self.dynamic_agents[j].collidable:
                        if self.dynamic_agents[i].collidesWith(self.dynamic_agents[j]):  
                            print(self.dynamic_agents[j])
                            agent1 = self.find_agent_by_car(self.dynamic_agents[i], agents)
                            agent2 = self.find_agent_by_car(self.dynamic_agents[j], agents)                                                      
                            return [agent1, agent2]
                for j in range(len(self.static_agents)):
                    if self.dynamic_agents[i].collidable and self.static_agents[j].collidable:
                        if self.dynamic_agents[i].collidesWith(self.static_agents[j]):
                            return []
            return []
        
        if not agent.collidable: return []

        for i in range(len(self.agents)):
            if self.agents[i] is not agent and self.agents[i].collidable and agent.collidesWith(self.agents[i]):
                return self.agents[i]
        return []    
    
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
    
    def run(self, autonomous_agents, n_max_cars): 
        active_agents = autonomous_agents[:n_max_cars]
        next_agent_index = n_max_cars
        arrived_count = 0
        collided_count = 0

        for aut in active_agents: 
            self.add(aut.car) 
            aut.update()
            aut.update_current_road()        
        start_time = time.time()

        while True:            
            if time.time() - start_time > TIME:
                break
            if not active_agents:
                break            
            for aut in active_agents:
                aut.update()
            self.tick() 
            self.render()
            time.sleep(TIMESTEP)

            # Remove agents that arrived to final destination or are involved in a collision
            arrived_agents = [agent for agent in active_agents if not agent.car.movable]
            collision_agents = self.collision_exists(autonomous_agents)
            arrived_count += len(arrived_agents)
            collided_count += len(collision_agents)
            to_remove = set(arrived_agents + collision_agents)

            if to_remove:
                active_agents = [agent for agent in active_agents if agent not in to_remove]
                for agent in to_remove:
                    self.delete_dynamic_agent(agent.car)

                # Add new agents to replace the ones that were removed
                while len(active_agents) < n_max_cars and next_agent_index < len(autonomous_agents):
                    new_agent = autonomous_agents[next_agent_index]
                    active_agents.append(new_agent)                    
                    self.add(new_agent.car)
                    new_agent.update()
                    new_agent.update_current_road()   
                    next_agent_index += 1
                                     
        print(f"Arrived: {arrived_count}, Collided: {collided_count}")
    
    def close(self):
        self.reset()
        self.static_agents = []
        if self.visualizer.window_created:
            self.visualizer.close()
        
    def reset(self):
        self.dynamic_agents = []
        self.t = 0
