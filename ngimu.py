'''
NGIMU Demo python v2.7 script written by Tom Mitchell (teamxe.co.uk) 2016
Requires pyOSC https://trac.v2.nl/wiki/pyOSC
'''

import socket, OSC, threading, time

# Change this to the NGIMU IP address
send_address = '192.168.1.1', 9000

# Set the NGIMU to send to this machine's IP address
c = OSC.OSCClient()
c.connect(send_address)
msg = OSC.OSCMessage()
msg.setAddress('/wifi/send/ip')
msg.append(str(socket.gethostbyname(socket.gethostname())))
c.send(msg)
c.close()

# Set up receiver
receive_address = '0.0.0.0', 8000
s = OSC.OSCServer(receive_address)
s.addDefaultHandlers()

def sensorsHandler(add, tags, args, source):
	print add + str(args)

def quaternionHandler(add, tags, args, source):
    print add + str(args)

def batteryHandler(add, tags, args, source):
	print add + str(args)

# Add OSC handlers
s.addMsgHandler("/sensors", sensorsHandler)
s.addMsgHandler("/quaternion", quaternionHandler)
s.addMsgHandler("/battery", batteryHandler)

# Start OSCServer
print "\nUse ctrl-C to quit."
st = threading.Thread(target = s.serve_forever)
st.start()

# Loop while threads are running
try :
	while 1 :
		time.sleep(10)

except KeyboardInterrupt :
	print "\nClosing OSCServer."
	s.close()
	print "Waiting for Server-thread to finish"
	st.join()
	print "Done"
