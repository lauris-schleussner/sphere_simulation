import ConfigReader
import SimobjectFactory
import Simulator

def main():
    """
    Main der Simulation. Diese Datei wird als erstes ausgeführt.
    Sie ist verantwortlich für das Lesen der Config.yaml Datei, das Erstellen der Simulationsobjekte
    und das Initialisieren/Starten der Simulation.
    """

    # read and check validity
    config = ConfigReader.ConfigReader.read()

    # create simobjects
    spheres = SimobjectFactory.SimobjectFactory.createSpheres(config["SIMOBJECTS"])
    cubes = SimobjectFactory.SimobjectFactory.createCubes(config["SIMOBJECTS"])

    # initialize Simulator and add simobjects
    simulator = Simulator.Simulator(config["GENERAL"])
    simulator.addObjects(spheres)
    simulator.addObjects(cubes)
    simulator.start()

if __name__ == "__main__":
    main()