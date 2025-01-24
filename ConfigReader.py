import yaml

class ConfigReader:
    """
        Klasse die eine config.yaml Datei einließt und als dict zurück gibt
    """
    
    @staticmethod
    def read():
        with open("config.yaml", 'r') as file:
            config = yaml.safe_load(file)
        return config