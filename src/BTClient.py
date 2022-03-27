import threading
import subprocess as sp
from .Configuration import Configuration
from .logger import get_logger

class BTClient(threading.Thread):
    '''
        Class which controls Bluetooth clients
        - allowed MACs from config.json
        By default:
          Allowed
    '''

    def __init__(self, config_file = "config.json", allowed = True, *args):
        super().__init__(daemon=False)
        self.allowed_devices = None
        self.lock = threading.Lock()
        self.allowed_devices = self.read_allowed_bluetooth_devices_from_config(config_file)
        self.logger = get_logger("BTClient")

        with self.lock:
            sp.check_output(["sudo", "service", "bluetooth", "restart"])

        self.logger.debug(f"BTClient created and bluetooth restarted{self}")

    def is_connected(self):
        return self.sniff_connection()
        if allowed:
            try:
                t = threading.Thread(target=self.sniff_connection, args=args)
                t.start()
                t.join()
            except Exception as e:
                self.logger.error(e)

    def sniff_connection(self):
        try:
            stdoutdata = sp.check_output(["hcitool", "con"])
            #self.logger.debug(f'1st global: {is_connected}\t self: {self.is_connected}')
            #self.logger.debug(bytes(allowestdoutdata.split())
            for allowed_mac in self.allowed_devices:
                if bytes(allowed_mac, 'utf-8') in stdoutdata.split():
                    #self.logger.debug(f"1conencted {allowed_mac}\t{is_connected}")
                    return True
                    #self.logger.debug(f"2conencted {allowed_mac}\t{is_connected}")
            return False
            #self.logger.debug(f'2nd global: {is_connected}\t self: {self.is_connected}')
        except Exception as e:
            self.logger.error("Check hcitool con output")
            self.logger.error(e)

    def read_allowed_bluetooth_devices_from_config(self, config_file):
        try:
            return Configuration.read_config_file(config_file)["allowed_bluetooth"]
        except Exception as e:
            self.logger.error("Check configuration")
            self.logger.error(e)
        return
