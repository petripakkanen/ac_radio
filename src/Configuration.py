import json

class Configuration():
    @staticmethod
    def read_config_file(config_file):  # -> Dict str, Any
        config = {}
        with open(config_file, 'r') as config_file:
            config = json.loads(config_file.read())
        return config
