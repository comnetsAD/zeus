import os
import time
import subprocess
import sys

TIME=60
DIR='output'
NUM_RUNS=1
exp = 'prot'

for prot in ["cubic","reno","bbr"]:
	os.system("sudo sysctl -w net.ipv4.tcp_congestion_control={0}".format(prot))
	for trace in os.listdir('traces/5G new format'):
		for i in range(1,NUM_RUNS+1):
			print (trace)
			buf_len = 1_000_000

			os.system('python run.py -tr {0} -t {1} --name {0}_{2}_{3}BDP --buf {4} --dir {5} --algo {6} --exp {2}'.format(trace,TIME,i,0,buf_len,DIR, prot, exp))
