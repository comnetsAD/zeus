#!/bin/bash

for prot in cubic bbr reno; do
	cd $prot;
	for file in */; do
		if ! [ -d $dir ]; then
			continue
		fi
		echo $file
		cd $file
		# tshark -r ReceiverTPUT.pcap -T fields -e frame.time_epoch -e frame.len 'ip.src==10.224.41.90' 2>/dev/null > throughputs.csv 
		tshark -r ReceiverTPUT.pcap -T fields -e frame.time_epoch -e frame.len 'ip.src==10.224.41.90' > throughputs.csv 
		tshark -r senderRTT.pcap -Y 'tcp.analysis.ack_rtt && ip.dst==10.224.41.90 && tcp.port>=60000' -T fields -e frame.time_epoch -e tcp.analysis.ack_rtt 2>/dev/null > delays.csv 
		cd ..
	done
	cd ..
done
