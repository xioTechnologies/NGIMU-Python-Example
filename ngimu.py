#NGIMU UDP Demo Python 3 script
#Requires python-osc 1.7.0 https://pypi.org/project/python-osc/

import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="0.0.0.0", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=8000, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
#  dispatcher.map("/sensors", print)
  dispatcher.map("/quaternion", print)
#  dispatcher.map("/battery", print)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()
