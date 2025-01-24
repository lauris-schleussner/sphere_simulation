import numpy as np
import math
import itertools
import view
import vpython as vp
import Simobjects

class Simulator:
    """
    3D Physiksimulator der die Interaktionen zwischen beweglichen Kugeln, starren Würfeln und den Wänden der Simulationsumgebung simuliert.
    Es werden elastische und inelastische Kollisionen unterstützt
    Die Kollisionsauflösung findet nach dem Impulserhaltungssatz statt
    """

    def __init__(self, general_config):
        self.simobjects = []
        self.time = 0
        self.general_config = general_config

        # configurable 
        self.size = general_config["size"]
        self.timestep = general_config["time_step"]
        self.restitution = general_config["restitution"]

    def addObjects(self, objects):
        """
        Füge Objekte zur Simulation hinzu
        """
        
        for simobject in objects:
            self.simobjects.append(simobject)

    def resolveSphereCubeCollisions(self, simobjects):
        """
        Kollisionsauflösung für Kugel mit Würfel
        
        Zuerst wird der Würfelpunkt berechnet, welcher der Kugel am nächste ist. Ausgehend von diesem kann anschließend 
        die Distanz und Penetrationstiefe berechnet werden.
        
        Die Kugel wird nach einer Kollision außerhalb des Würfels platziert, indem diese entlang der Kollisionsnormale verschoben wird
        Der neue Bewegungsvektor wird entsprechend der Formel berechnet. Da sich nur die Kugel bewegt lässt sich die vereinfachte Variante wählen, 
        wobei die Bewegung an der kolisionsnormale gespiegelt, und die Bewegungsrichtung invertiert wird. 
        
        v' = v - (1 + E) * (v x n) * n
        
        v' : Neuer Bewegungsvektor
        v : Alter Bewegungsvektor
        E : Elastizität
        (v x n) : Kreuzprodukt
        n : Kolisionsnormale 
        """
        
        # get cubes and spheres in seperate lists
        spheres = [obj for obj in simobjects if isinstance(obj, Simobjects.Sphere)]
        cubes = [obj for obj in simobjects if isinstance(obj, Simobjects.Cube)]
        
        for sphere in spheres:
            for cube in cubes:
                # Calculate cube's min and max corners from center
                half_side = cube.sidelength / 2
                cube_min = cube.position - half_side
                cube_max = cube.position + half_side
                
                # Find closest point on cube surface to sphere center
                closest_point = np.clip(sphere.position, cube_min, cube_max)
                
                # Compute distance
                distance = np.linalg.norm(sphere.position - closest_point)
                
                # Collision check using surface distance
                if distance < sphere.radius:
                    # Compute penetration depth and collision normal
                    penetration_depth = sphere.radius - distance
                    collision_normal = (sphere.position - closest_point) / (distance if distance > 0 else 1)
                    
                    # Resolve penetration
                    sphere.position = sphere.position + penetration_depth * collision_normal
                    
                    # Reflect velocity
                    velocity_along_normal = np.dot(sphere.movement, collision_normal)
                    sphere.movement = sphere.movement - (1 + self.restitution) * velocity_along_normal * collision_normal
                
    def resolveSphereSphereCollisions(self, simobjects):
        """
        Kolisionsauflösung zwischen zwei Kugeln
        
        Um Doppelberechnung zu vermeiden werden zuerst alle Kugelpaarkombinationen generiert. (1,2) => (2,1) nicht enthalten 
        Für jedes Paar wird deren 3D Distanz berechnet. Ist diese kleiner als die Summer der Radi liegt eine Kollision vor.
        
        Kollision wenn: ||A - B|| < r_A + r_B
        
        Um Doppeltberechnung bei Edgecases zu vermeiden, wird überprüft ob sich die beiden Kugeln entlang der Kolisionsnormale bereits voneinander entfernen.
        Fliegen sie nichtmehr aufeinander zu, kann die folgende Berechnung übersprungen werden.
        
        Der Impulsbetrag der Kollision wird berechnet. Dabei wird die relative Geschwindigkeit, sowie Masse mit einbezogen 
        
        |p| = (-(1 + E) * ((v_A - v_B) x n)) / (1/m_A + 1/m_B)
        
        |p| : Betrag des impulses
        E : Elastizität
        v_A, v_B Bewegungsvektoren
        n : Kollisionsnormale
        m_A/m_B : Massen
        
        Der Impuls wird für beide Objekte entland der Kolisionsnormale berechnet und je nach Masse skaliert. Jenachdem von welcher 
        Seite die Kolision betrachtet wird, wird der impuls addiert/subtrahiert
        
        p = |p| * n
        
        v' = v +- p/m  
        
        Eine Kolision wird erst festgestellt, nachdem sich zwei kugeln bereits geschnitten haben. Um für dies zu korrigieren,
        werden Die Kugeln entland der Kolisionsnormalen um einen kleinen Korrekturwert zurückgesetzt.
        
        d_p = r_A + r_B - ||A - B||
        
        A' = A +- d_p/2 * n
        
        d_p : Penetrationstiefe
        r_A, r_B : Radi
        ||A-B|| : distanz zwischen Mittelpunkten der Kugeln A und B
        A', A : Position der Kugel
        n : kolisionsnormale
        
        
        """
        
        # only select spheres
        all_pairs= itertools.combinations([obj for obj in simobjects if isinstance(obj, Simobjects.Sphere)], r = 2)
        collisions = []

        # check for collisions
        for A, B in all_pairs:
            d = np.linalg.norm(A.position - B.position)
            if d <= A.radius + B.radius:
                collisions.append([A,B])
        
        # resolve collisions
        for A, B in collisions:
            # Calculate collision normal
            collision_normal = (A.position - B.position) / np.linalg.norm(A.position - B.position)

            # Relative velocity along the normal
            relative_velocity = A.movement - B.movement
            velocity_along_normal = np.dot(relative_velocity, collision_normal)

            # Skip if objects are separating
            if velocity_along_normal > 0:
                continue

            # Calculate restitution and mass-related terms
            impulse_magnitude = -(1 + self.restitution) * velocity_along_normal
            impulse_magnitude /= 1 / A.weight + 1 / B.weight

            # Apply impulses to each object
            impulse = impulse_magnitude * collision_normal
            A.movement = A.movement + impulse / A.weight
            B.movement = B.movement - impulse / B.weight

            # Adjust positions slightly to resolve overlap
            penetration_depth = (A.radius + B.radius) - np.linalg.norm(A.position - B.position)
            correction = (penetration_depth / 2) * collision_normal
            A.position = A.position + correction
            B.position = B.position - correction

    def resolveSphereWallCollisions(self, simobjects):
        """
        Kolisionsauflösung zwischen Kugel und Wand. Da die Wände klar definiert sind, können die Kordinaten mit dem Kugelradius überprüft werden
        Eine Kolision findet statt, wenn entweder die Obere oder untere Wand berührt wird. Dies wird für alle 3 Freiheitsgrade berechnet.
        
        A.x - r_A <= 0
        A.x + r_A >= x_max
        
        A.x : X Kordinate der Kugel A
        r_A : Radius der Kugel A
        x_max : x Kordinate der Wand
        
        Da die Ebenen immer parallel zu den Achsen liegen, müssen bei Kolision nur einzelne Komponenten der Bewegung invertiert werden.
        
        Da auch hier eine Penetration der Wände passiert, wird die Kugel zunächst eine radiuslänge von der Wand in Kolisionsnormalenrichtung bewegt.
        Bei schrägen Kolisionen entsteht hier eine geringfügige Abweichung, da die Bewegung in andere Achsenrichtungen nicht berücksichtigt wird.
        Im nächsten Schritt wird die Bewegungskomponente in Kolisionsnormalenrichtung invertiert. Dadurch wird die Bewegung an der Wand reflektiert
        
        A.x = r_A       neue Position durch verändern der x Komponente bei Kolision mit x-Begrenzung
        v.x' = -v.x     Neuer Bewegungsvektor durch invertieren der x Komponente bei KOlision mit x-Begrenzung
        """
        
        spheres = [obj for obj in simobjects if isinstance(obj, Simobjects.Sphere)]
        
        for obj in spheres:
            x, y, z = obj.position
            radius = obj.radius

            # Wall collision logic with boundaries
            if x - radius <= 0:
                obj.position[0] = radius  # Correct position
                obj.movement[0] = -obj.movement[0] * self.restitution  # Reflect velocity

            if x + radius >= self.size:
                obj.position[0] = self.size - radius
                obj.movement[0] = -obj.movement[0] * self.restitution

            if y - radius <= 0:
                obj.position[1] = radius
                obj.movement[1] = -obj.movement[1] * self.restitution

            if y + radius >= self.size:
                obj.position[1] = self.size - radius
                obj.movement[1] = -obj.movement[1] * self.restitution

            if z - radius <= 0:
                obj.position[2] = radius
                obj.movement[2] = -obj.movement[2] * self.restitution

            if z + radius >= self.size:
                obj.position[2] = self.size - radius
                obj.movement[2] = -obj.movement[2] * self.restitution
            

    def advanceMovement(self):
        """
        Für jeden Zeitschritt werden die Kugeln entlang ihres Bewegungsvektors bewegt
        
        A' = A  + v_A * delta_T
        
        """
        for simobject in self.simobjects:
            if isinstance(simobject, Simobjects.Sphere):
                simobject.position = simobject.position + (simobject.movement * self.timestep)

    def _collision_normal(self, A, B):
        """
        Hilfsfunktion zur Berechnung der Kollisionsnormalen
        
        n = B-A / |B-A|
        
        B, A : Mittelpunkte zweier Objekte
        n : normierter Kollisionsvektor
        """
        
        n = B - A
        mag = np.linalg.norm(n)
        if (mag == 0):
            raise ValueError("Two collided objects are at the same location (colission vector = 0)")

        return n/mag 
    
    def _debug(self):
        for obj in self.simobjects:
            print(obj)

    def start(self):
        """
        Simulationsfunktion
        
        Für jeden Zeitschritt werden die folgenden Schritte ausgeführt:
        
            1. Simulationszeit erhöhen
            2. Kugel-Kugel Kolisionen behandeln
            3. Kugel-Wand Kollisionen behandeln
            4. Kugel-Würfel Kolisionen behandeln
            5. Szene rendern 
        """

        renderer = view.View(self.general_config)

        while True:
                # self._debug()
                
                self.time += self.timestep
                self.resolveSphereSphereCollisions(self.simobjects)
                self.resolveSphereWallCollisions(self.simobjects) 
                self.resolveSphereCubeCollisions(self.simobjects)
                self.advanceMovement()
                
                vp.rate(60)
                renderer.render(self.simobjects)           