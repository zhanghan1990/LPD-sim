#!/bin/bash
## This is the DCTCP simulation result
path=$1
tcl_script="$path/searchdctcp"; 
rm -rf $destdir
destdir=DCTCP
mkdir $destdir
load=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
sim_end=1000;
cap=10;
link_delay=0.0000002;
host_delay=0.0000025;
queueSize=150;
connections_per_pair=8;
meanFlowSize=1138*1460;

enableMultiPath=1;
perflowMP=0;

sourceAlg="DCTCP-Sack"
ackratio=1;
slowstartrestart=true;
DCTCP_g=0.0625;
min_rto=10000;

switchAlg=RED;

DCTCP_K=65;  ## In dctcp ,we set K =15
drop_prio_=false;
deque_proi_=false;

prio_scheme=2;
prob_mode_=0;
keep_order_=false;

topology_spt=10;
topology_tors=6;
topology_spines=2;
topology_x=(1 2 3 4 5 6 7 8 9 10);

enableNAM=0;

numcores=8;
trial=$2;

#This is the ns Path

ns="/home/zhanghan/ns-pfabric/ns-allinone-2.34/bin/ns";
for((test=0;test<$trial;test++))
 do
  cur_test_=$test
  for((m=0; m<${#topology_x[*]}; m++))
    do
      cur_topology_x_=${topology_x[$m]}
      for ((n=0; n<${#load[*]}; n++))
       do
  	  cur_load_=${load[$n]}
          curdir_=$cur_test_-$cur_topology_x_-$cur_load_-Ex
	  mkdir  $curdir_
	  $ns $tcl_script.tcl $sim_end $cap $link_delay $host_delay $queueSize $cur_load_  $connections_per_pair $meanFlowSize $enableMultiPath $perflowMP $sourceAlg $ackratio $slowstartrestart $DCTCP_g $min_rto $switchAlg $DCTCP_K $drop_prio_ $prio_scheme $deque_proi_ $prob_mode_ $keep_order_ $topology_spt $topology_tors $topology_spines $cur_topology_x_ $enableNAM
	  cp flow.tr DCTCP-$curdir_-flow.tr
          mv flow.tr $curdir_
          mv $curdir_ $destdir
          mv DCTCP-$curdir_-flow.tr $destdir
       done
    done
 done



