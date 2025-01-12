import ConfigReader
import SphereFactory
import Simulator

def main():

    # read and check validity
    simulation_data = ConfigReader.ConfigReader.read_and_check()

    spheres = SphereFactory.SphereFactory.createSpheres(simulation_data)

    simulator = Simulator.Simulator(simulation_data)
    simulator.setup(spheres)
    simulator.start()

if __name__ == "__main__":
    main()