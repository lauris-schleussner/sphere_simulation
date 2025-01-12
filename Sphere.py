import numpy as np

class Sphere:
    def __init__(self, id, radius, weight, color, position, movement):
        self.id = id
        self.radius = radius
        self.weight = weight
        self.color = color
        self.position = position
        self.movement = movement

    def set_position(self, position):
        self.position = np.array(position)
    
    def set_movement(self, movement):
        self.movement = np.array(movement)

    def __repr__(self):
        return f"Sphere (id = {self.id}, position = {self.position}, movement = {self.movement}, radius = {self.radius})"
    
    def get_position(self):
        return self.position
    
    def get_movement(self):
        return self.movement