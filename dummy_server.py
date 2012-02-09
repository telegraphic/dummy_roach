"""
Dummy_server.py
--------

This is a dummy KATCP roach server that responds to katcp requests ?read and ?write
This is designed for testing scripts without the need to connect to a roach.

"""

from katcp import DeviceServer, Sensor
from katcp.kattypes import Str, Float, Int, Timestamp, Discrete, request, return_reply
import time, struct, os
import cPickle as pkl

server_host = "localhost"
server_port = 7147

class MyServer(DeviceServer):

    VERSION_INFO = ("dummy-server", 1, 0)
    BUILD_INFO = ("hipsr-dummy-server", 0, 1, "")

    def setup_sensors(self):
        """Setup some server sensors."""

        self._time_result = Sensor(Sensor.TIMESTAMP, "time.result",
            "Last ?time result.", "")

        self._read_result = Sensor(Sensor.STRING, "read.result",
            "Last ?read result.", "")
        
        self._write_result = Sensor(Sensor.STRING, "write.result",
            "Last ?write result.", "")


        self.add_sensor(self._time_result)
        self.add_sensor(self._read_result)
        self.add_sensor(self._write_result)

    @request()
    @return_reply(Timestamp())
    def request_time(self, sock):
        """Return the current time in ms since the Unix Epoch."""
        r = time.time()
        self._time_result.set_value(r)
        return ("ok", r)

    @request(Str(),Int(),Int())
    @return_reply(Str())
    def request_read(self, sock, device_name, bytes, offset=0):
        """Dummy implementation of kactp ?read command
        
        Opens a pickled data file stored in /snap directory,
        and returns a packed struct of the data.
        
        Notes
        -----
        * The pickle should already be packed as a struct.
        * Currently ignoring the bytes and offset arguments.
        """
        # Attempt to load pickled data
        try:
           filename='%s/registers/%s.pkl'%(os.getcwd(),device_name)
           data   = pkl.load(open(filename,'r'))
        except:
           return ("fail", "Could not load %s."%filename)
        
        # Return data    
        self._read_result.set_value(data)
        return ("ok", data)
        
    @request(Str(),Int(),Str())
    @return_reply(Str())
    def request_write(self, sock, device_name, offset, data):
        """Dummy implementation of kactp ?write command
        
        Opens a pickled data file stored in /register directory,
        and writes a value to it.
        
        Notes
        -----
        * katcp_wrapper passes us already serialzed data, so no need to use struct
        """
        
        # Attempt to dump pickled data
        try:
          filename='%s/registers/%s.pkl'%(os.getcwd(),device_name)
          pkl.dump(data, open(filename,'w'))
        
        except:
          return ("fail", "Could not dump %s."%filename)

        return ("ok", data)



if __name__ == "__main__":
    
    print "Starting server on %s, port %i"%(server_host,server_port)
    server = MyServer(server_host, server_port)
    server.start()
    server.join()
