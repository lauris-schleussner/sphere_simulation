import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from Sphere import Sphere

# Initialize GLFW
def init_glfw():
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")
    
    window = glfw.create_window(800, 600, "OpenGL Sphere Simulation", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create GLFW window")
    
    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)  # Enable depth testing
    
    # Perspective projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800 / 600, 0.1, 50.0)  # Near and far clipping planes
    glMatrixMode(GL_MODELVIEW)
    
    return window

# Main render function
def render(spheres):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Set up the camera
    gluLookAt(15, 15, 15,  # Camera position (outside the box)
               0,  0,  0,     # Look at the center of the box
               0,  1,  0)     # Up direction (positive Y-axis)

    # Render all spheres
    for sphere in spheres:
        glPushMatrix()
        glTranslatef(*sphere.position)
        glColor3f(1.0, 0.0, 0.0)
        quadric = gluNewQuadric()
        gluSphere(quadric, sphere.radius, 32, 32)
        gluDeleteQuadric(quadric)
        glPopMatrix()
    glfw.swap_buffers(window)


if __name__ == "__main__":
    
    # Initialize GLFW and create a window
    window = init_glfw()
    

    # Main loop
    while not glfw.window_should_close(window):
        # Update sphere positions (e.g., simple oscillation for demo)
        for sphere in spheres:
            sphere.position = sphere.position + sphere.movement * 0.01

            # Render the frame
            render(spheres)

        # Poll events


    # Cleanup
    glfw.terminate()