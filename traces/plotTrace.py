import matplotlib.pyplot as plt
import os

trace_dir = "traces/5G new format"
traces = os.listdir(trace_dir)

def parse_Bandwidth_capacity(filename):

    f1 = open (filename,"r")
    BW = []
    nextTime = 1000
    cnt = 0
    for line in f1:
        a=line.split()
        if line == '\n':
            break
        if int(a[0]) > nextTime:
            BW.append((cnt*1516*8)/1000000)
            cnt = 0
            nextTime+=1000
        else:
            cnt+=int(a[1])
    f1.close()
    return BW

BW_cap = parse_Bandwidth_capacity(trace_dir + traces[0])

ax2 = plt.subplot()
ax2.set_facecolor('white')
ax2.fill_between(range(len(BW_cap)), 0, BW_cap,color='#D3D3D3',edgecolor="black")
# ax2.xaxis.set_major_locator(FixedLocator(np.arange(0, 61, 10)))
# ax2.yaxis.set_major_locator(FixedLocator(np.arange(0, 901, 300)))
ax2.set_xlabel('Time (s)', fontsize=10)
ax2.set_ylabel('Throughput (Mbps)', fontsize=10)
ax2.tick_params(axis='both', which='major', labelsize=10)

plt.savefig("5G2.png")
plt.show()