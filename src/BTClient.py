import threading
import subprocess as sp
from .Configuration import Configuration

class BTClient(threading.Thread):
    '''
        Class which controls Bluetooth clients
        - allowed MACs from config.json
        By default:
          Allowed
    '''

    def __init__(self, config_file = "config.json", allowed = True, *args):
        super().__init__(daemon=True)
        self.is_connected = False
        self.allowed_devices = None
        self.lock = threading.Lock()
        self.allowed_devices = self.read_allowed_bluetooth_devices_from_config(config_file)

        if allowed:
            try:
                t = threading.Thread(target=self.sniff_connection, args=args)
                t.start()
            except Exception as e:
                print(e)
        print(f"BTClient created {self}")

    def sniff_connection(self):
        try:
            stdoutdata = sp.check_output(["hcitool", "con"])
            for allowed_mac in self.allowed_devices:
                if bytes(allowed_mac, 'utf-8') in stdoutdata.split():
                    self.is_connected = True
                else:
                    self.is_connected = False
        except Exception as e:
            print("Check hcitool con output")
            print(e)

    def read_allowed_bluetooth_devices_from_config(self, config_file):
        try:
            return Configuration.read_config_file(config_file)["allowed_bluetooth"]
        except Exception as e:
            print("Check configuration")
            print(e)
        return
