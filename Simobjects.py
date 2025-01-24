import numpy as np

class Sphere:
    """
    Sphere Klasse enthält alle wichtigen Attribute für eine Kugel. Die Objekte werden in der SimobjectFactory erstellt.
    Die Attribute position und movement werden in der Simulation verändert
    """
    def __init__(self, id, radius, weight, color, position, movement):
        self.id = id
        self.radius = radius
        self.weight = weight
        self.color = color
        self.position = position
        self.movement = movement
        
    # better print()
    def __repr__(self):
        return f"Sphere (id = {self.id}, position = {self.position}, movement = {self.movement}, radius = {self.radius})"
    
class Cube:
    """
    Cube Klasse enthält alle wichtigen Attribute für eine Würfel. Die Objekte werden in der SimobjectFactory erstellt.
    """
    def __init__(self, id, color, position, sidelength):
        self.id = id
        self.color = color
        self.position = position # midpoint
        self.sidelength = sidelength
        
    def __repr__(self):
        return f"Cube (id = {self.id}, position = {self.position}, sidelength = {self.sidelength})"