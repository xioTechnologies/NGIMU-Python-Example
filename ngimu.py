import socket, threading, time, sys, argparse
from pythonosc import udp_client, dispatcher, osc_server

def process_arguments(argv):
	parser = argparse.ArgumentParser(description="NGIMU python example")
	parser.add_argument(
		"--ip",
		default="192.168.1.1",
		help="NGIMU IP Address")
	parser.add_argument(
		"--port",
		type=int,
		default=9000,
		help="NGIMU Port")
	parser.add_argument(
		"--receive_port",
		type=int,
		default=8910,
		help="Port to receive messages from NGIMU to this computer")

	return parser.parse_args(argv[1:])

#https://ubuntuforums.org/showthread.php?t=821325
def get_address():
    try:
        address = socket.gethostbyname(socket.gethostname())
        # On my system, this always gives me 127.0.1.1. Hence...
    except:
        address = ''
    if not address or address.startswith('127.'):
        # ...the hard way.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('4.2.2.1', 0))
        address = s.getsockname()[0]
    return address

def main(argv):
	args = process_arguments(argv)

	# Set the NGIMU to send to this machine's IP address
	client = udp_client.SimpleUDPClient(args.ip, args.port)
	client.send_message('/wifi/send/ip', get_address())
	client.send_message('/wifi/send/port', args.receive_port)

	def sensorsHandler(add, gx, gy, gz, ax, ay, az, mx, my, mz, b):
		print('{} g[{},{},{}] a[{},{},{}] m[{},{},{}] b[{}]'.format(
			add, gx, gy, gz, ax, ay, az, mx, my, mz, b))

	def quaternionHandler(add, x, y, z, w):
		print('{} [{},{},{},{}]'.format(add, x, y, z, w))

	def batteryHandler(add, pct, tte, v, i, state):
		print('{}, {}%, remaining: {}, v:{}, i:{}, {}'.format(
			add, pct, tte, v, i, state))

	def earthHandler(add, n, w, u):
		print('{}, [{},{},{}]'.format(add, n, w, u))

	def linearHandler(add, x, y, z):
		print('{}, [{},{},{}]'.format(add, x, y, z))

	dispatch = dispatcher.Dispatcher()
	dispatch.map('/sensors', sensorsHandler)
	dispatch.map('/quaternion', quaternionHandler)
	dispatch.map('/battery', batteryHandler)
	dispatch.map('/earth', earthHandler)
	dispatch.map('/linear', linearHandler)

	# Set up receiver
	receive_address = get_address(), args.receive_port
	server = osc_server.ThreadingOSCUDPServer(receive_address, dispatch)

	print("\nUse ctrl-C to quit.")
	# Start OSCServer
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.start()

	# Loop while threads are running
	try :
		while 1 :
			time.sleep(1)

	except KeyboardInterrupt :
		server.shutdown()
		server_thread.join()
		return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
