set ns [new Simulator]
if {$argc != 27} {
    puts "wrong number of arguments $argc"
    exit 0
}

set sim_end [lindex $argv 0]
set link_rate [lindex $argv 1]
set mean_link_delay [lindex $argv 2]
set host_delay [lindex $argv 3]
set queueSize [lindex $argv 4]
set load [lindex $argv 5]
set connections_per_pair [lindex $argv 6]
set meanFlowSize [lindex $argv 7]
#### Multipath
set enableMultiPath [lindex $argv 8]
set perflowMP [lindex $argv 9]
#### Transport settings options
set sourceAlg [lindex $argv 10] ; # Sack or DCTCP-Sack
set ackRatio [lindex $argv 11]
set enableHRTimer 0
set slowstartrestart [lindex $argv 12]
set DCTCP_g [lindex $argv 13] ; # DCTCP alpha estimation gain
set min_rto [lindex $argv 14]
#### Switch side options
set switchAlg [lindex $argv 15]
set DCTCP_K [lindex $argv 16]
set drop_prio_ [lindex $argv 17]
set prio_scheme_ [lindex $argv 18]
set deque_prio_ [lindex $argv 19]
set prob_cap_ [lindex $argv 20]
set keep_order_ [lindex $argv 21]
#### topology
set topology_spt [lindex $argv 22]
set topology_tors [lindex $argv 23]
set topology_spines [lindex $argv 24]
set topology_x [lindex $argv 25]
#### NAM
set enableNAM [lindex $argv 26]

#### Packet size is in bytes.
set pktSize 1460
#### trace frequency
set queueSamplingInterval 0.0001

################# Transport Options ####################

Agent/TCP set ecn_ 1
Agent/TCP set old_ecn_ 1
Agent/TCP set packetSize_ $pktSize
Agent/TCP/FullTcp set segsize_ $pktSize
Agent/TCP/FullTcp set spa_thresh_ 0
Agent/TCP set windowInit_ 2
Agent/TCP set slow_start_restart_ $slowstartrestart
Agent/TCP set windowOption_ 0
Agent/TCP set tcpTick_ 0.000001
Agent/TCP set minrto_ $min_rto

Agent/TCP/FullTcp set nodelay_ true; # disable Nagle
Agent/TCP/FullTcp set segsperack_ $ackRatio; 
Agent/TCP/FullTcp set interval_ 0.000006
if {$perflowMP == 0} {  
    Agent/TCP/FullTcp set dynamic_dupack_ 0.75
}
if {$ackRatio > 2} {
    Agent/TCP/FullTcp set spa_thresh_ [expr ($ackRatio - 1) * $pktSize]
}
if {$enableHRTimer != 0} {
    Agent/TCP set minrto_ 0.00100 ; # 1ms
    Agent/TCP set tcpTick_ 0.000001
}

#Shuang
Agent/TCP/FullTcp set prio_scheme_ $prio_scheme_;
Agent/TCP set window_ 1000000
Agent/TCP set windowInit_ 12
Agent/TCP set rtxcur_init_ $min_rto;
Agent/TCP/FullTcp/Sack set clear_on_timeout_ false;
#Agent/TCP/FullTcp set pipectrl_ true;
Agent/TCP/FullTcp/Sack set sack_rtx_threshmode_ 2;

set myAgent "Agent/TCP/FullTcp/Sack";


if {[string compare $sourceAlg "DCTCP-Sack"] == 0} {
    Agent/TCP set ecnhat_ true
    Agent/TCPSink set ecnhat_ true
    Agent/TCP set ecnhat_g_ $DCTCP_g;
}



################# Switch Options ######################

Queue set limit_ $queueSize

Queue/DropTail set queue_in_bytes_ true
Queue/DropTail set mean_pktsize_ [expr $pktSize+40]
Queue/DropTail set drop_prio_ $drop_prio_
Queue/DropTail set deque_prio_ $deque_prio_
Queue/DropTail set keep_order_ $keep_order_

Queue/RED set bytes_ false
Queue/RED set queue_in_bytes_ true
Queue/RED set mean_pktsize_ $pktSize
Queue/RED set setbit_ true
Queue/RED set gentle_ false
Queue/RED set q_weight_ 1.0
Queue/RED set mark_p_ 1.0
Queue/RED set thresh_ $DCTCP_K
Queue/RED set maxthresh_ $DCTCP_K
Queue/RED set drop_prio_ $drop_prio_
Queue/RED set deque_prio_ $deque_prio_

Agent/TCP/FullTcp/Sack/TimelyTCP  set v_high_ 500

Agent/TCP/FullTcp/Sack/TimelyTCP  set v_low_ 50
		 

Agent/TCP/FullTcp/Sack/TimelyTCP  set threshold_ 10


#DelayLink set avoidReordering_ true

############### NAM ###########################
if {$enableNAM != 0} {
    set namfile [open out.nam w]
    $ns namtrace-all $namfile
}

############## Multipathing ###########################

if {$enableMultiPath == 1} {
    $ns rtproto DV
    Agent/rtProto/DV set advertInterval	[expr 2*$sim_end]  
    Node set multiPath_ 1 
    if {$perflowMP != 0} {
	Classifier/MultiPath set perflow_ 1
    }
}



set S [expr $topology_spt * $topology_tors]
for {set i 0} {$i < $S} {incr i} {
    set sender($i) [$ns node]
}

set nqueue [$ns node]   
set receiver [$ns node] 

set S [expr $topology_spt * $topology_tors] 

for {set i 0} {$i < $S} {incr i} {
 $ns simplex-link $sender($i) $nqueue [set link_rate]Gb [expr $host_delay + $mean_link_delay] $switchAlg
 $ns simplex-link $nqueue $sender($i) [set link_rate]Gb [expr $host_delay + $mean_link_delay] $switchAlg
}

$ns simplex-link $receiver $nqueue  [set link_rate]Gb [expr $host_delay + $mean_link_delay] $switchAlg
$ns simplex-link $nqueue $receiver  [set link_rate]Gb [expr $host_delay + $mean_link_delay] $switchAlg


#############  Agents#########################

puts "Setting up connections ..."; flush stdout


for {set i 0} {$i < $S} {incr i} {
  set tcps($i) [new $myAgent]  ;# Sender TCP
  set tcpr($i) [new $myAgent]  ;# Receiver TCP
  $tcps($i) set fid_ [expr $i]
  $tcpr($i) set fid_ [expr $i]
  $ns attach-agent $sender($i) $tcps($i);
  $ns attach-agent $receiver $tcpr($i);
  $tcpr($i) listen
  $ns connect $tcps($i) $tcpr($i)
}

set flowmon [$ns makeflowmon Fid]
set MainLink [$ns link $nqueue $receiver]

$ns attach-fmon $MainLink $flowmon

set fcl [$flowmon classifier]

$ns at 0.1 "classifyFlows"

proc classifyFlows {} {
    global S fcl flowstats
    puts "NOW CLASSIFYING FLOWS"
    for {set i 0} {$i < $S} {incr i} {
	set flowstats($i) [$fcl lookup autp 0 0 $i]
    }
} 


set throughputSamplingInterval [expr 0.00048+($host_delay + $mean_link_delay)*4]

set qfile [$ns monitor-queue $nqueue $receiver [open queue.tr w] $throughputSamplingInterval]

proc throughputTrace {file} {
    global ns throughputSamplingInterval qfile flowstats S flowClassifyTime qmon tcps
    
    set now [$ns now]
     puts -nonewline $file "$now "
    for {set i 0} {$i < $S} {incr i} {
        $qmon($i) instvar barrivals_
        puts -nonewline $file "[expr $barrivals_/$throughputSamplingInterval*8/1000000]  "
        set barrivals_ 0
   }
   
  for {set i 0} {$i < $S} {incr i} {
        set cwnd [$tcps($i)  set cwnd_]
        puts -nonewline $file "$cwnd "
        set barrivals_ 0
   }
   


    $qfile instvar parrivals_ pdepartures_ pdrops_ pkts_ ss  
    puts  $file "[expr $parrivals_-$pdepartures_-$pdrops_]"    
    $ns at [expr $now+$throughputSamplingInterval] "throughputTrace $file"
}


for {set i 0 } {$i < $S} {incr i} {
  set qmon($i) [$ns monitor-queue $sender($i) $nqueue  [open queue.tr w] $throughputSamplingInterval ]
}




puts "Initial agent creation done.....";flush stdout
puts "Simulation started...."


set step  0.2
set T [expr $sim_end/$step]

#add jitter here
set   rng   [new RNG]
$rng   seed   0
set r3 [new RandomVariable/Uniform]
$r3    use-rng     $rng
$r3    set     min_       0.001
$r3    set     max_       0.01

set bytes 8000
puts $bytes
for {set i 0} {$i < $T} {incr i} {
   set Se [expr ($i+1)*5]
   for {set j 0} {$j < $Se} {incr j} {
        set    number [$r3 value]
	$ns at  [expr $i*$step+0.4] " $tcps($j) advanceby [expr $bytes/$Se]"
  }
}


#$ns at 0.9 "$tcps(0) advanceby 1000
#$ns at 0.5 "$tcps(1) advanceby 1000"
#$ns at 0.5 "$tcps(2) advanceby 1000"
#$ns at 0. "$tcps(3) advanceby 1000"

set throughputfile [open queue w]

$ns at $throughputSamplingInterval "throughputTrace $throughputfile"
$ns at $sim_end "finish"



proc finish {} {
        global ns enableNAM namfile mytracefile throughputfile
        $ns flush-trace
        close $throughputfile
        if {$enableNAM != 0} {
	    close $namfile
	    exec nam out.nam &
	}
	exit 0
}






$ns run
