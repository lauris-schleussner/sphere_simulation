import numpy as np
import math
import itertools
import view

# contains all the logic for SimObjects interacting with eachother
class Simulator:

    def __init__(self, general_data):
        self.simobjects = []
        self.time = 0

        self.xsize = general_data["GENERAL"]["xsize"]["value"]
        self.ysize = general_data["GENERAL"]["ysize"]["value"]
        self.zsize = general_data["GENERAL"]["zsize"]["value"]
        self.timestep = general_data["GENERAL"]["time_step"]["value"]
        self.gravity = general_data["GENERAL"]["gravity"]["value"]
        self.elasticity = general_data["GENERAL"]["elasticity"]["value"]

    def setup(self, objects):
         for simobject in objects:
            self.simobjects.append(simobject)

    def checkCollisions(self, simobjects):
        all_pairs= itertools.combinations(simobjects, r = 2)
        collisions = []

        for A, B in all_pairs:
            d = np.linalg.norm(A.position - B.position)
            if d <= A.radius + B.radius:
                collisions.append([A,B])

        return collisions
    
    # resolve collisions between objects
    def resolveCollisions(self, collided_objects):

        for A, B in collided_objects:
            n = self._collision_normal(A.position, B.position)
            new_velocity_A = A.movement - (2 * B.weight/ A.weight + B.weight) * ((A.movement - B.movement) * n) * n
            new_velocity_B = B.movement + (2 * A.weight/ A.weight + B.weight) * ((A.movement - B.movement) * n) * n
            print("Sphere collisiosn detected")

            A.set_movement(new_velocity_A)
            B.set_movement(new_velocity_B)

    def detectAndHandleWallCollisions(self, simobjects):
        for simobject in simobjects:
            x, y, z = simobject.position
            radius = simobject.radius

            newvelocity = np.array([])

            x_pos_norm = np.array([-1,0,0])
            x_neg_norm = np.array([1,0,0])
            y_pos_norm = np.array([0,-1,0])
            y_neg_norm = np.array([0,1,0])
            z_pos_norm = np.array([0,0,-1])
            z_neg_norm = np.array([0,0,1])

            
            if x - radius <= 0:
                simobject.position = simobject.position - simobject.movement * self.timestep # move back one timestep
                newvelocity = simobject.movement - (2 * np.dot(simobject.movement, x_pos_norm) * x_pos_norm)

            if x + radius >= self.xsize:
                simobject.position = simobject.position - simobject.movement * self.timestep
                newvelocity = simobject.movement - (2 * np.dot(simobject.movement, x_neg_norm) * x_neg_norm)  

            if y - radius <= 0:
                simobject.position = simobject.position - simobject.movement * self.timestep
                newvelocity = simobject.movement - (2 * np.dot(simobject.movement, y_pos_norm) * y_pos_norm)  

            if y + radius >= self.xsize:
                simobject.position = simobject.position - simobject.movement * self.timestep
                newvelocity = simobject.movement - (2 * np.dot(simobject.movement, y_neg_norm) * y_neg_norm)  

            if z - radius <= 0:
                simobject.position = simobject.position - simobject.movement * self.timestep
                newvelocity = simobject.movement - (2 * np.dot(simobject.movement, z_pos_norm) * z_pos_norm)  

            if z + radius >= self.zsize:
                simobject.position = simobject.position - simobject.movement * self.timestep
                newvelocity = simobject.movement - (2 * np.dot(simobject.movement, z_neg_norm) * z_neg_norm)  

            if len(newvelocity) != 0:
                simobject.set_movement(newvelocity)
            
    def advanceMovement(self):
        for simobject in self.simobjects:
            simobject.position = simobject.position + (simobject.movement * self.timestep)



    def _collision_normal(self, A, B):
        n = B - A
        mag = np.linalg.norm(n)
        if (mag == 0):
            raise ValueError("Two collided objects are at the same location (colission vector = 0)")

        return n/mag 

                
    def start(self):

        renderer = view.View()

        while True:
            self.time += self.timestep
            colissions = self.checkCollisions(self.simobjects)
            self.resolveCollisions(colissions)

            self.detectAndHandleWallCollisions(self.simobjects) 

            self.advanceMovement()

            renderer.render(self.simobjects)           