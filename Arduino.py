import sys
import glob
import serial
from time import sleep


class Arduino(object):
    port = None
    connection = None
    def connect(self):
        if not self.port is None and not self.connection is None:
            return True
        
        self.port = None
        self.connection = None
        try:
            data = self.get_ports()
            print data
            self.port = data[0]
            self.connection = serial.Serial(self.port, 115200)
            print self.connection.name
            return True
        except Exception:
            return False
        
    def get_ports(self):
        ports = glob.glob('/dev/tty.*')

        result = []
        for port in ports:
            if 'tty.wchusbserial14' in port:
                try:
                    s = serial.Serial(port)
                    s.close()
                    result.append(port)
                except (OSError, serial.SerialException):
                    pass
        return result
    def sendPacket(self, packet):
        self.connect()
        self.connection.write(packet)