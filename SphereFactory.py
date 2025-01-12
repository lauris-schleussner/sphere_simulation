import Sphere
import numpy as np

class SphereFactory:
 
    @staticmethod
    def createSpheres(configdata):

        sphere_list = []

        for key, value in configdata["SIMOBJECTS"].items():
            mass = value["mass"]["value"]
            radius = value["radius"]["value"]
            color = value["color"]
            motion = np.array(value["motion_vector"]["value"])
            position = np.array(value["position_vector"]["value"])

            sphere = Sphere.Sphere(
                id=int(key[9:]),
                radius=radius,
                weight=mass,
                color=color,
                position=position,
                movement=motion
            )

            sphere_list.append(sphere)

        return sphere_list