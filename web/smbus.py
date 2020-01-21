
class SMBus:
    def __init__(self, bus_nr):
        self.bus_nr = bus_nr

    def read_byte(self, address):
        return 42

    def write_byte(self, address, value):
        pass