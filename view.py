import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import Sphere
import vpython as vp

class View:

    def __init__(self, spheres) -> None:
        self.scene = vp.canvas(title="Spheres Render", width=800, height=600, background=vp.color.white)
        self.spheres = spheres
        self.vp_spheres =  [vp.sphere(pos=vp.vector(*sphere.position), radius=sphere.radius, color=vp.color.red) for sphere in spheres]

    def render(self, spheres):
        
        for sphere, vp_sphere in zip(self.spheres, self.vp_spheres):
            vp_sphere.pos = vp.vector(*sphere.position)