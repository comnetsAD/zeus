import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import scipy.stats
import scipy.optimize


def mean_confidence_interval(data,confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1+confidence)/2., n - 1)
    return m,m-h,m+h

def scale(a):
    return a/1000000.0

def parse_Bandwidth_capacity(filename):

    f1 = open (filename,"r")
    BW = []
    nextTime = 1000
    cnt = 0
    for line in f1:
        a=line.split()
        #print line
        if line == '\n':
            break
        if nextTime >= 60000:
            break    
        if int(a[0]) > nextTime:
            BW.append((cnt*1516*8)/1000000)
            cnt = 0
            nextTime+=1000
        else:
            cnt+=int(a[1])
    f1.close()
    return BW

def parse_throughput(filename):

    f1 = open (filename,"r")

    SIZE = 1.0
    total = 0
    nextTime = SIZE
    capacity = []
    times = []
    startTime=-1

    content = f1.read().split("\n")

    for line in tqdm(content):
        if line == "":
            continue
            
        if "," in line:
            line = line.strip().split(",")
            line[1] = 1494
        else:
            line = line.strip().split()

        if startTime < 0:
            startTime = float(line[0])

        if float(line[0])-startTime > 60:
            break

        if float(line[0])-startTime > nextTime:
            if len(line) > 1:
                total += int(line[1])*8/1000000
            else:
                continue

            capacity.append(total)
            times.append(float(line[0])-startTime)
            total = 0
            nextTime += SIZE

            while float(line[0])-startTime > nextTime:
                capacity.append(0)
                times.append(float(line[0])-startTime)
                nextTime += SIZE
        else:
            if len(line) > 1:
                total += int(line[1])*8/1000000
    
    f1.close()


    return capacity, times


def parse_delay_kernel(filename):
    times = []
    delay = []
    delay_file = open(filename, "r")
    tokens = delay_file.readline().strip().split("\t")
    sTime = float(tokens[0])
    for line in delay_file:
        if float(tokens[0])-sTime > float(30.0):
            break
        else:    
            tokens = line.strip().split("\t")
            delay.append(float(tokens[1])*1000.0)
            times.append(float(tokens[0])-sTime)
    delay_file.close()
    return delay, times


def plot_scatter_compare(bdp, expt_prefix):

    plt.rc('pdf', fonttype=42)
    plt.rc('ps', fonttype=42)
    plt.rc('ps', useafm=True)
    plt.rc('pdf', use14corefonts=True)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    algo_list=["bbr", "cubic", "reno"]   
    NUM_RUNS = 1
    marker_dict = {'reno' : 'o', 'cubic' : 'x', 'bbr' : '*'}
    marker_color_dict = {'reno' : '#a6cee3', 'cubic' : '#1f78b4', 'bbr' : '#b2df8a'}

    for algo in tqdm(algo_list, desc='Reading tput and RTT files'):
        x = []
        y = []
        for i in range(1,NUM_RUNS+1):
            pathprefix = os.path.join(algo, expt_prefix+'_{0}_{1}BDP'.format(i, bdp))
            print(pathprefix)

            if not os.path.exists(pathprefix):
                continue

            print(algo)
            tput_kernel = []
            tput_times_kernel = []
            tput_kernel, tput_times_kernel = parse_throughput("{0}/throughputs.csv".format(pathprefix))
            df_tput = pd.DataFrame({'timestamp': tput_times_kernel, 'tput': tput_kernel} )   
            delay_kernel = []
            delay_times_kernel=[]
            delay_kernel, delay_times_kernel = parse_delay_kernel("{0}/delays.csv".format(pathprefix))
            print(pathprefix)
            df_rtt = pd.DataFrame({'timestamp':delay_times_kernel, 'rtt':delay_kernel})
            df_rtt.loc[:, 'rtt'] = df_rtt.rtt.values # convert RTT to seconds                

            x.append(df_rtt.rtt.mean())
            y.append(df_tput.tput.mean())
            print('mean throughput =',y)
            print('mean delay =',x)

        mx, lx, hx = mean_confidence_interval(x)
        my, ly, hy = mean_confidence_interval(y)
        color = marker_color_dict[algo]
        marker = marker_dict[algo]

        ax.scatter(mx, my, marker=marker, s=250, color=color, edgecolors=['black'][0], label=algo, alpha=0.8)

    ax.grid()
    ax.set_xlabel('RTT (ms)')
    ax.set_ylabel('Throughput (Mbps)')
    ax.xaxis.get_ticklocs(minor=True)
    plt.legend(loc='lower right', prop={'size': 12})
    ax.set_xlim(left=20)
    ax.set_ylim(bottom=100, top=400)

    BW_cap = parse_Bandwidth_capacity("../traces/5G new format/{0}".format(trace))
    Av = np.mean(BW_cap)
    ax.text(125,Av-5, int(Av), color="red", fontsize=18, backgroundcolor="white",zorder=-100)
    plt.axhline(y=Av, color='r', linestyle='dashed',zorder=-101)

    
    # channel in-set
    l, b, h, w = .3, .27, .25, .25    
    ax2 = fig.add_axes([l, b, w, h])
    ax2.set_facecolor('white')
    ax2.fill_between(range(len(BW_cap)), 0, BW_cap,color='#D3D3D3',edgecolor="black")
    ax2.set_xlabel('Time (s)', fontsize=10)
    ax2.set_ylabel('Throughput (Mbps)', fontsize=10)
    ax2.tick_params(axis='both', which='major', labelsize=10)


    # fig.savefig(f'{expt_prefix}.pdf', bbox_inches='tight')
    plt.show()

    return

if __name__ == '__main__':

    params = {
              'font.size' : 20,
              'legend.fontsize': 4,
              }
    plt.rcParams.update(params)

    plt.rcParams['ytick.labelsize'] = 20
    plt.rcParams['xtick.labelsize'] = 20

traces = os.listdir('../traces/5G new format')
for trace in traces:
    for bdp in [0]:
        plot_scatter_compare(bdp, trace)
