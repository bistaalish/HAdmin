import telnetlib
import logging


class Huawei:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.telnet = None

    def connect(self):
        """Connect to the Huawei OLT via Telnet."""
        try:
            self.telnet = telnetlib.Telnet(self.host)
            self.telnet.read_until(b"Username:")
            self.telnet.write(self.username.encode('ascii') + b"\n")
            self.telnet.read_until(b"Password:")
            self.telnet.write(self.password.encode('ascii') + b"\n")
            logging.info(f"Connected to OLT at {self.host}")
            return True
        except Exception as e:
            logging.error(f"Failed to connect to OLT: {e}")
            return False

    def send_command(self, command):
        """Send a command to the Huawei OLT."""
        try:
            if self.telnet:
                self.telnet.write(command.encode('ascii') + b"\n")
                return self.telnet.read_until(b">").decode('ascii')
            else:
                raise ConnectionError("Not connected to OLT.")
        except Exception as e:
            logging.error(f"Error sending command: {e}")
            return str(e)

    def disconnect(self):
        """Disconnect from the Huawei OLT."""
        if self.telnet:
            self.telnet.close()
            logging.info(f"Disconnected from OLT at {self.host}")
            self.telnet = None
