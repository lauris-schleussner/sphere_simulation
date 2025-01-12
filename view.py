import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import Sphere

class View:

    def __init__(self) -> None:
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio

    def render(self, spheres):
         
        self.ax.cla()  # Clear previous frame

        for i, sphere in enumerate(spheres):
            x,y,z = sphere.position
            r = sphere.radius
            color = sphere.color
            # print("sphere", i, "at", x, y, z)

            self.render_sphere(x, y,z, r, self.ax)

            # TODO get limits here
            self.ax.set_xlim([0, 10])
            self.ax.set_ylim([0, 10])
            self.ax.set_zlim([0, 10])

        plt.draw()
        plt.pause(0.0000000000001)


        
    def create_sphere(self, x, y, z, radius):
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        x_sphere = x + radius * np.outer(np.cos(u), np.sin(v))
        y_sphere = y + radius * np.outer(np.sin(u), np.sin(v))
        z_sphere = z + radius * np.outer(np.ones(np.size(u)), np.cos(v))
        return x_sphere, y_sphere, z_sphere

    # Function to render a sphere object
    def render_sphere(self, x, y, z, radius, ax):
        x_sphere, y_sphere, z_sphere = self.create_sphere(x, y, z, radius)
        ax.plot_wireframe(x_sphere, y_sphere, z_sphere, color='b', alpha=0.7)

