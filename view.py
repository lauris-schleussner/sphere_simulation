import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from Sphere import Sphere
import vpython as vp
import math

class View:

    def __init__(self):
        
        self.camera_angle = 0
        
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")
    
        self.window = glfw.create_window(800, 600, "OpenGL Sphere Simulation", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")
        
        glfw.set_key_callback(self.window, self.rotate_callback)
        
        glfw.make_context_current(self.window)
        glEnable(GL_DEPTH_TEST)  # Enable depth testing
        
        # Perspective projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800 / 600, 0.1, 50.0)  # Near and far clipping planes
        glMatrixMode(GL_MODELVIEW)

    def draw_wireframe_box(self, center, size):
        x, y, z = center
        s = size

        # Draw the box's edges with GL_LINES (wireframe)
        glBegin(GL_LINES)
        glVertex3f(x - s, y - s, z - s)  # Front bottom-left
        glVertex3f(x + s, y - s, z - s)  # Front bottom-right

        glVertex3f(x + s, y - s, z - s)  # Front bottom-right
        glVertex3f(x + s, y - s, z + s)  # Back bottom-right

        glVertex3f(x + s, y - s, z + s)  # Back bottom-right
        glVertex3f(x - s, y - s, z + s)  # Back bottom-left

        glVertex3f(x - s, y - s, z + s)  # Back bottom-left
        glVertex3f(x - s, y - s, z - s)  # Front bottom-left

        glVertex3f(x - s, y + s, z - s)  # Front top-left
        glVertex3f(x + s, y + s, z - s)  # Front top-right

        glVertex3f(x + s, y + s, z - s)  # Front top-right
        glVertex3f(x + s, y + s, z + s)  # Back top-right

        glVertex3f(x + s, y + s, z + s)  # Back top-right
        glVertex3f(x - s, y + s, z + s)  # Back top-left

        glVertex3f(x - s, y + s, z + s)  # Back top-left
        glVertex3f(x - s, y + s, z - s)  # Front top-left

        glVertex3f(x - s, y - s, z - s)  # Front bottom-left
        glVertex3f(x - s, y + s, z - s)  # Front top-left

        glVertex3f(x + s, y - s, z - s)  # Front bottom-right
        glVertex3f(x + s, y + s, z - s)  # Front top-right

        glVertex3f(x + s, y - s, z + s)  # Back bottom-right
        glVertex3f(x + s, y + s, z + s)  # Back top-right

        glVertex3f(x - s, y - s, z + s)  # Back bottom-left
        glVertex3f(x - s, y + s, z + s)  # Back top-left
        glEnd()
            
            
    def update_camera(self):
            
        # Convert the angle to radians for trigonometric functions
        radians = math.radians(self.camera_angle)
        
        # Camera distance from the center (radius of the rotation)
        radius = 20
        
        # Calculate camera position in XZ-plane based on angle
        cam_x = radius * math.cos(radians) + 5 # plus half encolsure
        cam_z = radius * math.sin(radians) + 5
        
        # Set the camera view
        gluLookAt(cam_x, 7.5, cam_z,  # Camera position
                5, 5, 5,           # Look at the center of the box
                0, 1, 0)           # Up direction (positive Y-axis)
        
    def rotate_callback(self, window, key, scancode, action, mods):
        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
            self.camera_angle = (self.camera_angle + 1) % 360  # Increment angle by 1 degree

    # Main render function
    def render(self, spheres):
        glfw.poll_events()
        
        # check for end
        if glfw.window_should_close(self.window): glfw.terminate()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.update_camera()

        # Render all spheres
        for sphere in spheres:
            glPushMatrix()
            glTranslatef(*sphere.position)
            glColor3f(1.0, 0.0, 0.0)
            quadric = gluNewQuadric()
            gluSphere(quadric, sphere.radius, 32, 32)
            gluDeleteQuadric(quadric)
            glPopMatrix()
    
    
        glColor4f(0.0, 1.0, 0.0, 0.5)           # wireframe is green and transparent
        self.draw_wireframe_box([5, 5, 5], 5)   # Center at (5, 5, 5) with size 5
            
        glfw.swap_buffers(self.window)
        
        # Poll events
        glfw.poll_events()