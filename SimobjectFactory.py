import Simobjects
import numpy as np

class SimobjectFactory:
    """
    Factory Klasse zum erstellen der Simulationsobjekte. Diese werden aus dem "SIMOBJECT" Teil der Konfiguration erstellt.
    Die einzelnen Methoden erstellen jeweils ihr eigenes Objekt. Der Typ wird vom Feld "type" festgelegt.
    Die ID entspricht der verwendeten Nummer in der Configdatei: "SIMOBJEKT25" -> 25
    """
 
    @staticmethod
    def createSpheres(simobject_config):
        """
        Erstelle Sphere Objekte aus den Configdaten
        """

        # iterate over declared simobjects in the config file
        sphere_list = []
        for simobject_number, properties in simobject_config.items():
            
            if properties["type"] != "sphere": # skip non spheres
                continue
            
            # create Object
            sphere = Simobjects.Sphere(
                id=int(simobject_number[9:]),
                radius=properties["radius"],
                weight=properties["mass"],
                color=properties["color"],
                position=np.array(properties["position_vector"]),
                movement=np.array(properties["motion_vector"])
            )
            sphere_list.append(sphere)
        return sphere_list
    

    @staticmethod
    def createCubes(simobject_config):
        """
        Erstelle Cube Objekte aus den Configdaten
        """
        
        cubelist = []
        for simobject_number, properties in simobject_config.items():
            if properties["type"] != "cube":
                continue
            
            cube = Simobjects.Cube(
                id = int(simobject_number[9:]),
                color = properties["color"],
                sidelength = properties["sidelength"],
                position = np.array(properties["position_vector"])
            )
            cubelist.append(cube)
        return cubelist