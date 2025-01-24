import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from Simobjects import Sphere, Cube
import math

class View:
    """
    Rendering Klasse die die Sumulation darstellt. Sie bietet die render() methode, welche alle Simulationsobjekte übergeben bekommt
    die render() Funktion wird 1x pro Frame ausgeführt. Das Rendering wird von OPENGL mit GLUT durchgeführt und besteht aus 3 Komponenten:
    
        Kugeln : Unterstützen verschiedene Farben, Reflektionen, Schatten
        Würfel: Unterstützt verschiedene Farben, keine Reflektionen oder Schatten
        Wireframe: grün, ohne Lichtberechnung
         
    Das Sichtfeld passt sich automatisch der Simulationsgröße an.
    
    Durch Drücken der Leertaste kann um die Simulation rotiert werden.
    """

    def __init__(self, general_config):
        
        self.general_config = general_config
        self.camera_angle = 0 # camera direction 
        
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")
    
        self.window = glfw.create_window(800, 600, "OpenGL Sphere Simulation", None, None)
        
        # rotation around simulation by pressing SPACE
        glfw.set_key_callback(self.window, self._rotate_callback)
        glfw.make_context_current(self.window)
        
        # rendering Setup
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHT0)
        
        # Setup lighting position relative to Camera
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800 / 600, 0.1, 10000.0)
        glMatrixMode(GL_MODELVIEW)
        
        # set up lighting
        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        
        
    def draw_wireframe_box(self, center, size):
        """
        Die Äußeren Simulationsgrenzen werden über OPENGL Vertexe gezeichnet
        """
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
        """
        Kamerarichtung wird definiert. Die Position wird jeden Frame neu berechnet, da sich der Kamerawinkel verändern kann,
        indem die Kamera um die Simulation rotiert
        """
            
        # Convert the angle to radians for trigonometric functions
        radians = math.radians(self.camera_angle)
        
        # Camera distance from the center (radius of the rotation)
        radius = self.general_config["size"] * 1.8
        
        # Calculate camera position in XZ-plane based on angle
        cam_x = radius * math.cos(radians) + self.general_config["size"] / 2 # plus half encolsure
        cam_z = radius * math.sin(radians) + self.general_config["size"] / 2
        
        # Set the camera view
        gluLookAt(cam_x, 0.75 * self.general_config["size"], cam_z,  # Camera position
                self.general_config["size"]/2, self.general_config["size"]/2, self.general_config["size"]/2,           # Look at the center of the box
                0, 1, 0)           # Up direction (positive Y-axis)
        
    def _rotate_callback(self, window, key, scancode, action, mods):
        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
            self.camera_angle = (self.camera_angle + 1) % 360  # Increment angle by 1 degree
            
    def color_to_opengl(self, color_name):
        # Define a dictionary mapping common color names to RGBA values
        color_map = {
            "red": [1.0, 0.0, 0.0, 1.0],
            "green": [0.0, 1.0, 0.0, 1.0],
            "blue": [0.0, 0.0, 1.0, 1.0],
            "yellow": [1.0, 1.0, 0.0, 1.0],
            "cyan": [0.0, 1.0, 1.0, 1.0],
            "magenta": [1.0, 0.0, 1.0, 1.0],
            "black": [0.0, 0.0, 0.0, 1.0],
            "white": [1.0, 1.0, 1.0, 1.0],
            "gray": [0.5, 0.5, 0.5, 1.0],
            "orange": [1.0, 0.5, 0.0, 1.0],
            "purple": [0.5, 0.0, 0.5, 1.0],
        }

        # Return the corresponding RGBA value, or raise an error if unknown
        return color_map.get(color_name.lower(), None)
    
    
    def render(self, simobjects):
        """
        Rendering Funktion. Es wird nach folgender Reihenfolge vorgegangen:
        
            - Kugeln
            - Würfel
            - Wireframe
        """
        # Poll events and check for window close
        glfw.poll_events()
        if glfw.window_should_close(self.window):
            glfw.terminate()
        
        # reset scene for next frame
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # update Camera for a new Angle
        self.update_camera()

        # Set material properties applied to spheres
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [50.0])

        glEnable(GL_LIGHTING)  # Enable lighting

        # Render all spheres
        for sphere in simobjects:
            if not isinstance(sphere, Sphere): continue
            
            glPushMatrix()
            glTranslatef(*sphere.position)
            glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color_to_opengl(sphere.color))
            
            # Render sphere using quadrics
            quadric = gluNewQuadric()
            gluSphere(quadric, sphere.radius, 32, 32)
            gluDeleteQuadric(quadric)
            glPopMatrix()
            
        # render all cubes
        # reflections are not suppoerted
        for cube in simobjects:
            if not isinstance(cube, Cube): continue
            
            glDisable(GL_LIGHTING)
            glPushMatrix()
            glTranslatef(*cube.position)
            
            half = cube.sidelength / 2
            # Cube face rendering with explicit normals
            faces = [
                ((0, 0, 1), [(-half, -half, half), (half, -half, half), (half, half, half), (-half, half, half)]),
                ((0, 0, -1), [(-half, -half, -half), (-half, half, -half), (half, half, -half), (half, -half, -half)]),
                ((1, 0, 0), [(half, -half, -half), (half, -half, half), (half, half, half), (half, half, -half)]),
                ((-1, 0, 0), [(-half, -half, -half), (-half, half, -half), (-half, half, half), (-half, -half, half)]),
                ((0, 1, 0), [(-half, half, -half), (half, half, -half), (half, half, half), (-half, half, half)]),
                ((0, -1, 0), [(-half, -half, -half), (half, -half, -half), (half, -half, half), (-half, -half, half)])
            ]
            
            for normal, vertices in faces:
                glBegin(GL_QUADS)
                glNormal3f(*normal)
                for vertex in vertices:
                    glColor4fv(self.color_to_opengl(cube.color))
                    glVertex3f(*vertex)
                glEnd()
            
            glPopMatrix()

        # Wireframe 
        glDisable(GL_LIGHTING)       
        glColor3f(0.0, 0.9, 0.0)# wireframe is green and transparent
        
        # wireframe at center with length
        self.draw_wireframe_box([self.general_config["size"] / 2 for _ in range(3)], self.general_config["size"] / 2)   # Center at (5, 5, 5) with size 5
            
        glfw.swap_buffers(self.window)