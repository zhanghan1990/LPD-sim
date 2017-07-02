#!/bin/bash
## This is the DCTCP simulation result

load=(0.1)
sim_end=2;
cap=1;
link_delay=0.0000002;
host_delay=0.0000025;
queueSize=1000;
connections_per_pair=1;
meanFlowSize=1138*1460;

enableMultiPath=1;
perflowMP=0;

sourceAlg="DCTCP-Sack"
ackratio=1;
slowstartrestart=true;
DCTCP_g=0.0625;
min_rto=0.002;

switchAlg=DropTail;

DCTCP_K=65;  ## In dctcp ,we set K =15
drop_prio_=false;
deque_proi_=false;

prio_scheme=0;
prob_mode_=0;
keep_order_=false;

topology_spt=100;
topology_tors=1;
topology_spines=2;
topology_x=5;

enableNAM=0;

numcores=8;
trial=1;
tcl_script="/home/zhanghan/zhanghan/ns-pfabric/ex4/simpleDumbbell";     

top_dir="/home/zhanghan/zhanghan/ns-pfabric/ex4/test"



#This is the ns Path

ns="/home/zhanghan/pfabric-mahanmod/ns-pfabric/ns-allinone-2.34/bin/ns";


for ((n=0; n<${#load[*]}; n++))
do
	cur_load_=${load[$n]}
	ns $tcl_script.tcl $sim_end $cap $link_delay $host_delay $queueSize $cur_load_  $connections_per_pair $meanFlowSize $enableMultiPath $perflowMP $sourceAlg $ackratio $slowstartrestart $DCTCP_g $min_rto $switchAlg $DCTCP_K $drop_prio_ $prio_scheme $deque_proi_ $prob_mode_ $keep_order_ $topology_spt $topology_tors $topology_spines $topology_x $enableNAM
done




