import json
from .logger import get_logger

class Configuration():
    @staticmethod
    def read_config_file(config_file):  # -> Dict str, Any
        config = {}
        with open(config_file, 'r') as config_file:
            config = json.loads(config_file.read())
            get_logger().debug(f'Read config file: {config_file}\n{config}\n')
        return config
