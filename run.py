from subprocess import Popen, PIPE
from argparse import ArgumentParser
import os
from time import sleep


USER_NAME= ''
PASSWORD = ''
IP_ADDRESS = ''
FILE_TO_DOWNLOAD = ''

delay = 10


def Run_kernel():

	if not os.path.exists(args.dir + '/' + args.algo):
		os.makedirs(args.dir+ '/' + args.algo)
	if not os.path.exists(args.dir +  '/' + args.algo + '/' +str(args.name)):
		os.makedirs(args.dir+ '/' + args.algo + '/'+str(args.name))

	args.dir = args.dir+'/' + args.algo + '/'

	os.system("sudo tcpdump -i any -s 96 -w " + args.dir + "/" + args.name + "/senderRTT.pcap &")

	print("Begin " + str(args.time) + " seconds of Cubic transmission")

	# command = "mm-delay 10 mm-loss downlink 0.1 mm-link --meter-all ../traces/5G new format/" + str(args.trace) + " ../traces/5G new format/"  + str(args.trace) +" --downlink-queue=droptail --downlink-queue-args=bytes=9000000"
	command = f"mm-delay {delay} mm-link --meter-all traces/5G new format/" + str(args.trace) + " ../traces/5G new format/"  + str(args.trace)


	p = Popen(command, stdin=PIPE,shell=True)
	p.communicate("sudo tcpdump -i any -s 96 -w " + args.dir + "/" + args.name + "/ReceiverTPUT.pcap & \n wget ftp://{0}:{1}@{2}/{3} & \n sleep ".format(USER_NAME, PASSWORD, IP_ADDRESS, FILE_TO_DOWNLOAD) + str(args.time) + " \n exit")

	os.system("ps | pgrep -f wget | sudo xargs kill -9")
	os.system("ps | pgrep -f tcpdump | sudo xargs kill -9")
	sleep (5)

if __name__ == '__main__':
	parser = ArgumentParser(description="Shallow queue tests")
	parser.add_argument('--dir', '-d',help="Directory to store outputs",required=True)
	parser.add_argument('--trace', '-tr',help="Cellsim traces to be used",required=True)
	parser.add_argument('--time', '-t',help="Duration (sec) to run the experiment",type=int,default=10)
	parser.add_argument('--name', '-n',help="name of the experiment",required=True)
	parser.add_argument('--algo',help="Algorithm under which we are running the simulation",required=True)
	parser.add_argument('--command', '-c', help="mm-link command to run", required=False)                
	parser.add_argument('--exp', help='experimets between 2 CCAs')
	parser.add_argument('--buf', help='buffer size')
	args = parser.parse_args()
	Run_kernel()


