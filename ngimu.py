import socket, threading, time, sys, argparse
from pythonosc import udp_client, dispatcher, osc_server

def process_arguments(argv):
	parser = argparse.ArgumentParser(description="NGIMU python example")
	parser.add_argument(
		"--ip",
		default="192.168.1.1",
		help="NGIMU IP Adress")
	parser.add_argument(
		"--port",
		type=int,
		default=9000,
		help="NGIMU Port")

	return parser.parse_args(argv[1:])

def main(argv):
	args = process_arguments(argv)

	# Set the NGIMU to send to this machine's IP address
	client = udp_client.SimpleUDPClient(args.ip, args.port)
	client.send_message(
		'/wifi/send/ip',
		str(socket.gethostbyname(socket.gethostname())))

	def sensorsHandler(add, gx, gy, gz, ax, ay, az, mx, my, mz, b):
		print('{} g[{},{},{}] a[{},{},{}] m[{},{},{}] b[{}]'.format(
			add, gx, gy, gz, ax, ay, az, mx, my, mz, b))

	def quaternionHandler(add, x, y, z, w):
		print('{} [{},{},{},{}]'.format(add, x, y, z, w))

	def batteryHandler(add, pct, tte, v, i, state):
		print('{}, {}%, remaining: {}, v:{}, i:{}, {}'.format(
			add, pct, tte, v, i, state))

	dispatch = dispatcher.Dispatcher()
	#dispatch.map('/sensors', print)
	dispatch.map('/sensors', sensorsHandler)
	dispatch.map('/quaternion', quaternionHandler)
	dispatch.map('/battery', batteryHandler)

	# Set up receiver
	receive_address = str(socket.gethostbyname(socket.gethostname())), 8089
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
