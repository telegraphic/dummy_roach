"""
Dummy.py
--------

A virtual roach server that will respond to katcp requests
"""

from katcp import DeviceServer, Sensor
from katcp.kattypes import Str, Float, Timestamp, Discrete, request, return_reply
import time
import random

server_host = "localhost"
server_port = 7147

class MyServer(DeviceServer):

    VERSION_INFO = ("dummy-server", 1, 0)
    BUILD_INFO = ("hipsr-dummy-server", 0, 1, "")

    FRUIT = [
        "apple", "banana", "pear", "kiwi",
    ]

    BANDS = [
        "autolux", "nirvana", "acdc", "tool",
    ]


    def setup_sensors(self):
        """Setup some server sensors."""
        self._add_result = Sensor(Sensor.FLOAT, "add.result",
            "Last ?add result.", "", [-10000, 10000])

        self._time_result = Sensor(Sensor.TIMESTAMP, "time.result",
            "Last ?time result.", "")

        self._eval_result = Sensor(Sensor.STRING, "eval.result",
            "Last ?eval result.", "")

        self._fruit_result = Sensor(Sensor.DISCRETE, "fruit.result",
            "Last ?pick-fruit result.", "", self.FRUIT)

        self._band_result = Sensor(Sensor.DISCRETE, "band.result",
            "Last ?pick-band result.", "", self.BAND)


        self.add_sensor(self._add_result)
        self.add_sensor(self._time_result)
        self.add_sensor(self._eval_result)
        self.add_sensor(self._fruit_result)
        self.add_sensor(self._band_result)

    @request(Float(), Float())
    @return_reply(Float())
    def request_add(self, sock, x, y):
        """Add two numbers"""
        r = x + y
        self._add_result.set_value(r)
        return ("ok", r)

    @request()
    @return_reply(Timestamp())
    def request_time(self, sock):
        """Return the current time in ms since the Unix Epoch."""
        r = time.time()
        self._time_result.set_value(r)
        return ("ok", r)

    @request(Str())
    @return_reply(Str())
    def request_eval(self, sock, expression):
        """Evaluate a Python expression."""
        r = str(eval(expression))
        self._eval_result.set_value(r)
        return ("ok", r)

    @request()
    @return_reply(Discrete(FRUIT))
    def request_pick_fruit(self, sock):
        """Pick a random fruit."""
        r = random.choice(self.FRUIT + [None])
        if r is None:
            return ("fail", "No fruit.")
        self._fruit_result.set_value(r)
        return ("ok", r)

    @request()
    @return_reply(Discrete(BAND))
    def request_pick_band(self, sock):
        """Pick a random fruit."""
        r = random.choice(self.BAND + [None])
        if r is None:
            return ("fail", "No band.")
        self._fruit_result.set_value(r)
        return ("ok", r)


if __name__ == "__main__":

    server = MyServer(server_host, server_port)
    server.start()
    server.join()
