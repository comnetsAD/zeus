# Zeus Emulation Framework

This is a framework for the evaluation of Congestion Control protocols in 5G environments. The components of this framework required
for these experiments are explained below. Currently, this framework is only supported on Linux. 

## Channel Traces
The traces directory contains various 5G channel traces that were collected in the real world from a commercial 5G deployment.
The traces are available in the original Mahimahi format as well as our modified Mahimahi format, further explained below.


## Mahimahi

This framework uses Mahimahi to emulate the channel traces. The installation instructions for mahimahi are available at:
http://mahimahi.mit.edu/

The original Mahimahi platform is not optimized for 5G environments, so it is recommended to install the version linked below following the same
instructions mentioned on the original website for building from the source code.
Optimized format link: `git clone -b batch-packets --single-branch https://github.com/rohailasim123/mahimahi.git`

## Experiment application

We use the bftpd server as our application for our evaluation. The framework can also be modified to use other applications such as iperf3
or any customized server and client program.

In order to use bftpd, the repository is linked below and the bftpd.conf configuration file and the passwd file needs to be modified. 
Detailed installation and running instructions are available on the original repository. 
BFTPD repository: https://github.com/gamman/bftpd

Once installed, the command to run the server is:  `sudo ./bftpd -D -c bftpd.conf`

## Running the experiment
Finally, once Mahimahi and the application server are ready, we can run the experiments using `run_exp.py` after updating the bftpd information in `run.py`. 
The current version of this repository is configured for protocols that are available in Linux in net.ipv4.tcp_available_congestion_control. Other protocols 
that are available as pluggable linux kernel modules can be added directly. For protocols that are not available as kernel modules, the code needs to be modified 
to run the application server and client program that supports the new protocol.


## Results

Once the experiment is finished, the results are available as pcap files in the output directory.

Using tshark, we can extract and plot these results. The scripts for these actions are available in the output directory.

Feel free to contact rohail.asim@nyu.edu with any questions or issues such as issues in running this program or issues in adding new congestion
control protocols.

Citation
--------
    @misc{asim2022zeus,
        author      = "Asim, Rohail and Khan, Muhammad and Diez, Luis and Iyer, Shiva and Aguero, Ramon and Subramanian, Lakshmi and Zaki, Yasir",
        title       = "ZEUS: An Experimental Toolkit for Evaluating Congestion Control Algorithms in 5G Environments",
        journal     = "arXiv e-prints",
        eprint      = "2208.13985",
        url         = "https://arxiv.org/abs/2208.13985"
        year        = "2022"
    }
