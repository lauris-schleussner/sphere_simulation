import yaml

class ConfigReader:
    def read_object_data():
        with open("config.yaml", 'r') as file:
            config = yaml.safe_load(file)

        return config

    def process_config(config_data):
        # Iterate through all the general settings
        for key, item in config_data['GENERAL'].items():
            value = item['value']
            constraint = item['constraint']
            ConfigReader.check_constraint(value, constraint)

        # Iterate through all the SIMOBJECTS
        for sim_object, object_data in config_data['SIMOBJECTS'].items():
            for key, item in object_data.items():
                if key in ['color']:  # Skip color, no constraints to check
                    continue
                value = item['value']
                constraint = item['constraint']
                ConfigReader.check_constraint(value, constraint)


    def check_constraint(value, constraint):
        if isinstance(value, list):
            if len(value) != 3: raise ValueError("missing value, expected [x,y,z] vector")

            for v in value:
                if not (constraint[0] < v < constraint[1]):
                    raise ValueError(f"Value {v} is out of range {constraint} for {value}")
        else:
            if not (constraint[0] < value < constraint[1]):
                raise ValueError(f"Value {value} is out of range {constraint} for {value}")
            

    def read_and_check():
        config = ConfigReader.read_object_data()
        ConfigReader.process_config(config)

        return config