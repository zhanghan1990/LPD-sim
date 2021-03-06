source basic_functions.tcl


# input parameters
set mice_load    [expr [lindex $argv 0]]; # diff mice loads
set pruning      [expr [lindex $argv 1]]; # pruning (0-false, 1-true)
set delegation   [expr [lindex $argv 2]]; # delegation (0-false, 1-true)
set ArbsInRack   [expr [lindex $argv 3]];
set av_fsize     [expr [lindex $argv 4]]; # avg flow size in KB
set sim_time     [expr [lindex $argv 5]];
set SRC            [lindex $argv 6];


set STATS_INTR 0.0003
set STATS_INTR_CBQ 0.0003
set STATS_START 0.0

set dctcp_enable 1 ; # enable DCTCP
set AlltoAllFlows 0
set simpleFlows 1
set shortFlowsInterRackThruAggs 0; # this flag indicates if we want to build flows that have the Agg Switch as their root
set getQmonQueueLevelStats 0; # [PASE ONLY] 1 if we want Queue Monitoring at the CBQ queue level at agg-core links
set getQmonLinkLevelStats 0; # this is set to 1 if we want the Queue Monitoring at link level for agg->core links

# Bandwidth of each layer defined here # over-subscription factor is going to be around 1:8 or 1:10 initially
set bw_endhostTor 1000.0 ; # currently we want 1Gbps bw between endhost-TOR
set bw_torAgg 10000.0 ; # currently we want 1Gbps bw between TOR-aggregator
set bw_aggCore 10000.0 ; # currently we want 1Gbps bw between aggregator-core

set num_cores 1; # total number of cores
set num_aggs 2; # number of aggregator switches per core switch
set num_tors 2; # number of ToR switches per aggregator switch
set num_hosts 40; # number of endhosts per rack --> later change it to 20

if {$SRC == "TCP/CTP"} {
	set SINK "TCPSink/Sack1/CtpSink"
	set cbq_enable 1 ; # [PASE ONLY] to enable CBQ links 
	set separate_arbs 0
	Node set pruning 0
	Node set  delegation 0
	puts "Sink = $SINK !"

	if { $delegation == 1 } {
		Node set  delegation 1
		Agent/TCP/PaseArbitrator set delegated_cap_o [expr $bw_aggCore/($num_aggs*1000)]
		Agent/TCP/PaseArbitrator set delegated_cap_i [expr $bw_aggCore/($num_aggs*1000)]
		puts "delegation set to true!"
	}
	if { $pruning == 1 } {
		Node set pruning 1
		Node set pruning_prio 1
		puts "pruning set to true!"
		puts "pruning level 1"
	}
	if { $ArbsInRack == 1 } {
		set separate_arbs 1
		puts "separate arbs set to true!"
	}
} elseif {$SRC == "TCP/Sack1"} {
	set SINK "TCPSink/Sack1"
	set cbq_enable 0 ; # [PASE ONLY] to enable CBQ links 
	set separate_arbs 0
	Node set pruning 0
} else {
	set SINK "TCPSink/Sack1"
	set cbq_enable 0 ; # [PASE ONLY] to enable CBQ links 
	set separate_arbs 0
	Node set pruning 0
}



set link_delay 0.025; # per link delay, multiply by 12 to get RTT
set qLimit 250; # queue limit for our links
set numClasses 8; # number of classes for each CBQ Link
Node set num_ques $numClasses
puts "queue length = $qLimit"


set ftpFlowPerTor 1 ; # How many FTP flows per rack
set num_rev_flow 0 ; # TODO: currently not implemented

# General settings...
set pkSize 1000
set K 65; #65





# TCP specific settings...
Agent/TCP set tcpTick_ 0.0001

# DCTCP related things....
Agent/TCP set ecn_ 1
Agent/TCP set old_ecn_ 1
Agent/TCP set dctcp_ true
set DCTCP_g_ 0.0625 ; # EWMA weight of alpha
set ackRatio 1 ; # number of acks per data pkt
Agent/TCP set slow_start_restart_ false ; # slow_start_restart is FALSE
Agent/TCP set dctcp_g_ $DCTCP_g_; 

# use large timeouts for PASE
Agent/TCP set maxrto_ 1
Agent/TCP set minrto_ 0.2 ;
puts "RTO min 0.1 sec"	;	# Default changed to 200ms on 
Agent/TCP set rtxcur_init_ 0.03 ;
Agent/TCP set window_ 80

# small piece of code to set the bottleneck bandwidth.... could not get the min function of TCL!!??!!
set btnk_bw [expr $bw_aggCore]

# initializing RED parameters
Queue/RED set bytes_ false
Queue/RED set queue_in_bytes_ false ; 
Queue/RED set mean_pktsize_ $pkSize ; 
Queue/RED set setbit_ true
Queue/RED set gentle_ false
Queue/RED set q_weight_ 1.0
Queue/RED set mark_p_ 1.0
Queue/RED set thresh_ [expr $K]
Queue/RED set maxthresh_ [expr $K]

set arb_port 30; # get from user as well...

set totalHosts [expr $num_hosts * $num_tors * $num_aggs] ; # use this (div by 2) in place of hostsPerAgg


set ns [new Simulator]

# 1 core (maybe make this also variable later one for multiple paths scenario)
# num of aggregator switches = number of pods desired (variable), currently we may want to keep enought to reach total 1000 endhosts
# num of TOR switches per aggregator = variable, currently might keep it to 4
# num of hosts per rack = variable, currently thinking of 40 per rack

#			  ___
#			 |___| Core
#			/    \
#		       /      \
#		      |_|     |_| Agg
#		      /	\      / \
#		     /	 \    /   \
#		    |_|	 |_| |_|  |_| TOR
#		    / \  / \  / \  / \
#		    ....  ...  ...  .... Hosts
#
#	Core -> Agg [2 Aggs] (10G)
#	Agg -> TOR [2 TORs per Agg] (10G)
#	TOR -> Endhosts [20 hosts per rack] (1G)


#end-host: local arb-agent at port 20 (this port number can also be made a var)
#end-host: arb-agent at port $arb_port (currently we have $arb_port=30)
#TOR-switch: arb-agent-sink at any port (other than $arb_port)

#TOR-switch: arb-agent at port $arb_port (currently $arb_port=30)
#Agg-switch: arb-agent-sink at any port 

set f_u_t [open tor-agg_updates.txt w]
set f_u_e [open end-tor_updates.txt w]

#Define a 'finish' procedure
proc finish {} {
      global file_CBQ_allQ_util file_CBQ_allQ_drops file_CBQ_allQ_avgqlen file_CBQ_allQ_pkts numClasses Out SRC mice_load fq_mon f_util f_loss f_queue SRC f_u_t f_u_e num_cores num_tors num_aggs num_hosts paseArbInvokerTor paseArbInvokerHost getQmonLinkLevelStats getQmonQueueLevelStats host

	if {$getQmonLinkLevelStats == 1} {
		for { set i 0 } { $i < $num_cores } { incr i } {
			for { set j 0 } { $j < $num_aggs } { incr j } {
				set aggIndex [expr ($i*$num_aggs)+$j] 
				close $fq_mon($aggIndex)
				close $f_util($aggIndex)
				close $f_loss($aggIndex)
				close $f_queue($aggIndex)			
			}
		}
	}	
	if {$getQmonQueueLevelStats == 1} {
		for { set i 0 } { $i < $num_cores } { incr i } {
			for { set j 0 } { $j < $num_aggs } { incr j } {
				set aggIndex [expr ($i*$num_aggs)+$j] 
				close $file_CBQ_allQ_util($aggIndex)
				close $file_CBQ_allQ_drops($aggIndex)
				close $file_CBQ_allQ_avgqlen($aggIndex)
				close $file_CBQ_allQ_pkts($aggIndex)
			}
		}
	}
	## AFCT calculations
	close $Out

	set awk_response {
	BEGIN{
	    av=0;
	}
	{
	    drops += $11;
	    sum += $5;
	    nl += 1;
	}
	END{
	    printf "Number of lines = %f\n", nl;
	    printf "sum = %f\n", sum;
	    av = sum/nl;


	    printf "%s %.2f %s %.5f ms %d flows %d drops\n", type, load, src, av, nl, drops >> fil;

	}
    }
    
    set awk_util {
	BEGIN{
	    av=0;

	}
	{
	    sum += $2;
	    nl += 1;
	}
	END{
	    printf "Number of lines = %f\n", nl;
	    printf "sum = %f\n", sum;
	    av = sum/nl;
	    printf "%f %f\n", bw, av >> file;
	}
    }

	set awk_updates {
	BEGIN{
	    av=0;
	}
	{
	    sum += $1;
	    nl += 1;
	}
	END{
	    printf "sum = %f\n", sum;
	    printf "%.2f %i %i updates\n", load, enabled, sum >> fil;
	}
     }
    set to_read "Out.ns"
    set res "response_times.log"

    exec awk -v type="all" -v load=$mice_load -v src=$SRC -v fil=$res $awk_response $to_read

    if { $SRC == "TCP/CTP" } {
        #puts $f_u_t "PRUNING [$paseArbInvokerTor(0) set pruning] Load $mice_load"
        for { set k 0 } { $k < $num_tors*$num_aggs } { incr k } {
		    puts $f_u_t "[$paseArbInvokerTor($k) set updt_req_sent]\t [$paseArbInvokerTor($k) set nrexmit_]"
        }
        #puts $f_u_e "PRUNING [$paseArbInvokerHost(0) set pruning] Load $mice_load"
        for { set i 0 } { $i < $num_tors*$num_aggs*$num_hosts } { incr i } {
		    puts $f_u_e "[$paseArbInvokerHost($i) set updt_req_sent]\t [$paseArbInvokerHost($i) set nrexmit_]"
        }

		close $f_u_t
		close $f_u_e
		set to_read "tor-agg_updates.txt"
		set res "tor-aggr_updates.log"
		exec awk -v load=$mice_load -v enabled=[$host(0) set pruning] -v fil=$res $awk_updates $to_read

		set to_read "end-tor_updates.txt"
		set res "end-tor_updates.log"
		exec awk -v load=$mice_load -v anabled=0 -v fil=$res $awk_updates $to_read
    }
    exit 0
}


proc record {} {
	global file_CBQ_allQ_util file_CBQ_allQ_drops file_CBQ_allQ_avgqlen file_CBQ_allQ_pkts num_cores num_tors num_aggs bw_aggCore qmonAggCbq cbqPktCount numClasses timeIntsElapsed pkSize STATS_INTR_CBQ agg core

    set ns [Simulator instance] ;
    set timeElapse $STATS_INTR_CBQ;
    
    set now [$ns now]
	set den [expr 8/($timeElapse*1000000)]

	# this loop is assuming we have qmons equal to the number of ToR->Agg links
	#for { set i 0 } { $i < [expr $num_tors * $num_aggs] } { incr i } {
	#	puts -nonewline $file_qmonCBQ($aggIndex) "[$qmon($i) set parrivals_]\t"
	#}
	set timeIntsElapsed [expr $timeIntsElapsed + 1]

	for { set i 0 } { $i < $num_cores } { incr i } {
		for { set j 0 } { $j < $num_aggs } { incr j } {
			set aggIndex [expr ($i*$num_aggs)+$j] 
			#set torIndex [expr ($aggIndex*$num_tors)+$k]

			if {$aggIndex == 0} {
				
				#puts $fq1 [format "ave_=%.2f curq_=%.2f" [expr $q1($aggIndex) set ave_] [expr $q1($aggIndex) set curq_]]
				#puts $fq1 [format "curq_=%.2f" [expr $q1($aggIndex) set curq_]]
			}
		
			#print time here in the file_CBQ_allQ_util($aggIndex)
			set utilzSum 0; # sum for a particular link
			set dropsSum 0; # drop rate sum for a particular link
			set avgqlenSum 0; # sum of average q lengths for all queues on a link
			set pktsSum 0; # sum of current q lengths for a particular link
			puts -nonewline $file_CBQ_allQ_util($aggIndex) [format "Interval: %.5f-%.5f\t" [expr [$ns now] - $timeElapse] [$ns now]]
			puts -nonewline $file_CBQ_allQ_drops($aggIndex) [format "Interval: %.5f-%.5f\t" [expr [$ns now] - $timeElapse] [$ns now]]
			puts -nonewline $file_CBQ_allQ_avgqlen($aggIndex) [format "Interval: %.5f-%.5f\t" [expr [$ns now] - $timeElapse] [$ns now]]
			puts -nonewline $file_CBQ_allQ_pkts($aggIndex) [format "Interval: %.5f-%.5f\t" [expr [$ns now] - $timeElapse] [$ns now]]

			set monitoredLink [$ns link $agg($aggIndex) $core($i)]
	    	set bandw [[$monitoredLink link] set bandwidth_]			

			for { set cls 0 } { $cls < $numClasses } { incr cls } {
				set qmonIndex [expr ($aggIndex*$numClasses) + $cls]
			
				set utilz [expr 8*[$qmonAggCbq($qmonIndex) set bdepartures_]/[expr 1.*$timeElapse*$bandw]]
			
				if {[$qmonAggCbq($qmonIndex) set parrivals_] != 0} {
					set drprt [expr [$qmonAggCbq($qmonIndex) set pdrops_]/[expr 1.*[$qmonAggCbq($qmonIndex) set parrivals_]]]
				} else {
					set drprt 0
				}
				set cur_q_len [$qmonAggCbq($qmonIndex) set pkts_]
				set avg_q_len [expr [$qmonAggCbq($qmonIndex) set parrivals_] - [$qmonAggCbq($qmonIndex) set pdepartures_]]
				set cbqPktCount($qmonIndex) [expr $cbqPktCount($qmonIndex) + $cur_q_len]
				set avg_q_l [expr 1.0*$cbqPktCount($qmonIndex)/$timeIntsElapsed]
				
				set utilz [expr $utilz * 100]
				set drprt [expr $drprt * 100]

				set utilzSum [expr $utilzSum + $utilz]
				set dropsSum [expr $dropsSum + $drprt]
				set avgqlenSum [expr $avgqlenSum + $avg_q_len]
				set pktsSum [expr $pktsSum + $cur_q_len]


				puts -nonewline $file_CBQ_allQ_util($aggIndex) [format "%.2f\t" $utilz]
				puts -nonewline $file_CBQ_allQ_drops($aggIndex) [format "%.2f\t" $drprt]
				puts -nonewline $file_CBQ_allQ_avgqlen($aggIndex) [format "%.0f\t" $avg_q_len]
				puts -nonewline $file_CBQ_allQ_pkts($aggIndex) [format "%.0f\t" $cur_q_len]
				$qmonAggCbq($qmonIndex) reset
			}
			#do endline work here... for file_CBQ_allQ_util/drops($aggIndex)
			puts $file_CBQ_allQ_util($aggIndex) [format "Sum=%.2f" $utilzSum]
			puts $file_CBQ_allQ_drops($aggIndex) [format "Sum=%.2f" $dropsSum]
			puts $file_CBQ_allQ_avgqlen($aggIndex) [format "Sum=%.0f" $avgqlenSum]
			puts $file_CBQ_allQ_pkts($aggIndex) [format "Sum=%.0f" $pktsSum]
		}
	}

	$ns at [expr $now+$timeElapse] "record"
}

# this procedure creates the 2-way links between each child and parent node
Simulator instproc makeLink {childNode parentNode linkBW linkDelay pktSize cbqEnable qLimit qmonIndex} {
	global ns 

	if {$cbqEnable == 1} {
		# fwd path
		$ns simplex-link $childNode $parentNode [expr $linkBW]Mb [expr $linkDelay]ms CBQ
		$ns makeCBQlink $childNode $parentNode 1 $pktSize $qmonIndex
		#$ns queue-limit $childNode $parentNode $qLimit; # originally 100

		# rev path
		$ns simplex-link $parentNode $childNode [expr $linkBW]Mb [expr $linkDelay]ms CBQ
		$ns makeCBQlink $parentNode $childNode 1 $pktSize $qmonIndex
		#$ns queue-limit $parentNode $childNode $qLimit ; # originally 1000	
	} else {
		$ns duplex-link $childNode $parentNode [expr $linkBW]Mb [expr $linkDelay]ms RED
		$ns queue-limit $childNode $parentNode $qLimit
	}
}

#Setup CBQ structure
Simulator instproc makeCBQlink {node1 node2 timeLink pktSize qmonIndex} {
	global qmonAggCbq numClasses getQmonQueueLevelStats
	
	set th 65
	set th_2 65
	set limit 500

	set cbqlink [$self link $node1 $node2]

	for { set i 0 } { $i < $numClasses } { incr i } {
    	set lowerClass($i) [new CBQClass]
		set q($i) [new Queue/RED]

		$q($i) set bytes_ false
		$q($i) set queue_in_bytes_ false ; # IMP
		$q($i) set mean_pktsize_ $pktSize ; # IMP
		$q($i) set setbit_ true
		$q($i) set gentle_ false
		$q($i) set q_weight_ 1.0
		$q($i) set mark_p_ 1.0	
	   	$q($i) set thresh_ $th
		$q($i) set maxthresh_ $th
		$q($i) set thresh_queue_ $th_2
		$q($i) set maxthresh_queue_ $th_2
		if {$i > $numClasses-3} {
		#puts "setting limit to 500"
		$q($i) set limit_ 500
		} else {
		$q($i) set limit_ $limit
		}
		$lowerClass($i) install-queue $q($i)
		$lowerClass($i) setparams none false 1.0 auto $i 1 0;	# setparams parent okborrow allot maxidle prio level

		if {$qmonIndex >= 0 && $getQmonQueueLevelStats==1} {
			$cbqlink insert $lowerClass($i) $qmonAggCbq([expr ($qmonIndex*$numClasses) + $i])
		} else {
			$cbqlink insert $lowerClass($i) 
		}
 		$cbqlink bind $lowerClass($i) $i
	}
}

# this procedure installs the required arbitrator agents depending on whether it
# is an endhost or not, using the specified value of arbPort for the invoker-Agent
Simulator instproc addArbitrators {childNode parentNode endhostFlag arbPort arbInvoker} {
    global ns
    
	if {$endhostFlag == 1} {
		set paseArbLocal [new Agent/TCP/PaseArbitrator]
		$childNode attach $paseArbLocal 20 ; # the local arbitrator agent for an endhost
	}

    $childNode attach $arbInvoker $arbPort ; # the agent on childNode which invokes its parent arbitrator
    set paseArbRemoteAgent [new Agent/TCPSink/Sack1/PaseArbitratorSink]
    $parentNode attach $paseArbRemoteAgent
    $ns connect $arbInvoker $paseArbRemoteAgent ; # Connect the two agents

    $arbInvoker set packetSize_ 0; #newly added
}

# Begin: setup topology ----------------------------------------


# temporary piece of code
if {$ftpFlowPerTor == 0} {
	set ftpFlowPerTor [expr $num_hosts] ; # $num_ftp_flow per rack will be same as num of hosts per rack 
}

# this counter will count the number of times the stats for CBQ have been generated
set timeIntsElapsed 0

# Create core switches 
for { set i 0 } { $i < $num_cores } { incr i } {
	set core($i) [$ns node]
	if { $SRC == "TCP/CTP" } {
		$core($i) set level 3
	}
	# Create aggregator switches 
	for { set j 0 } { $j < $num_aggs } { incr j } {
		set aggIndex [expr ($i*$num_aggs)+$j] 
		set agg($aggIndex) [$ns node]
		if { $SRC == "TCP/CTP" } {
			$agg($aggIndex) set level 2
			$agg($aggIndex) set link_bw [expr ($bw_aggCore/1000.0)]
			if { $separate_arbs == 1 } {
				set aggArb($aggIndex) [$ns node]
				$aggArb($aggIndex) set level 2
				$aggArb($aggIndex) set link_bw [expr ($bw_aggCore/1000.0)]
			}
		}

		if {$cbq_enable==1 && $getQmonQueueLevelStats==1} {
			set fname_CBQ_allQ_util($aggIndex) "qmon.cbq_allQ_util_"
			set fname_CBQ_allQ_drops($aggIndex) "qmon.cbq_allQ_drops_"
			set fname_CBQ_allQ_avgqlen($aggIndex) "qmon.cbq_allQ_avgqlen_"
			set fname_CBQ_allQ_pkts($aggIndex) "qmon.cbq_allQ_curqlen_"	
			append fname_CBQ_allQ_util($aggIndex) "Ag$aggIndex"
			append fname_CBQ_allQ_util($aggIndex) "Co$i"
			append fname_CBQ_allQ_drops($aggIndex) "Ag$aggIndex"
			append fname_CBQ_allQ_drops($aggIndex) "Co$i"
			append fname_CBQ_allQ_avgqlen($aggIndex) "Ag$aggIndex"
			append fname_CBQ_allQ_avgqlen($aggIndex) "Co$i"
			append fname_CBQ_allQ_pkts($aggIndex) "Ag$aggIndex"
			append fname_CBQ_allQ_pkts($aggIndex) "Co$i"
			set file_CBQ_allQ_util($aggIndex) [open $fname_CBQ_allQ_util($aggIndex) w]
			set file_CBQ_allQ_drops($aggIndex) [open $fname_CBQ_allQ_drops($aggIndex) w]
			set file_CBQ_allQ_avgqlen($aggIndex) [open $fname_CBQ_allQ_avgqlen($aggIndex) w]
			set file_CBQ_allQ_pkts($aggIndex) [open $fname_CBQ_allQ_pkts($aggIndex) w]

			for { set cls 0 } { $cls < $numClasses } { incr cls } {
				set qmonAggCbq([expr ($aggIndex*$numClasses) + $cls]) [new QueueMonitor]
			}
		}

		$ns makeLink $agg($aggIndex) $core($i) $bw_aggCore $link_delay $pkSize $cbq_enable $qLimit $aggIndex

		if {$cbq_enable==1 && $getQmonQueueLevelStats==1} {
			for { set cls 0 } { $cls < $numClasses } { incr cls } {
				$ns at $STATS_START  "$qmonAggCbq([expr ($aggIndex*$numClasses) + $cls]) reset"
				set cbqPktCount([expr ($aggIndex*$numClasses) + $cls]) 0
			}
		}

		# Create TOR switches 
		for { set k 0 } { $k < $num_tors } { incr k } {
			set torIndex [expr ($aggIndex*$num_tors)+$k] 
			set tor($torIndex) [$ns node]
			if { $SRC == "TCP/CTP" } {
				$tor($torIndex) set level 1
				$tor($torIndex) set link_bw [expr ($bw_torAgg/1000.0)]
			}
			# links btw agg-TORs
			$ns makeLink $tor($torIndex) $agg($aggIndex) $bw_torAgg $link_delay $pkSize $cbq_enable $qLimit -1
			if { $SRC == "TCP/CTP" } {
				# add arbitrator agents
				set paseArbInvokerTor($torIndex) [new Agent/TCP/PaseArbitrator]

				if { $separate_arbs == 1 } {
					set torArb($torIndex) [$ns node]
					$torArb($torIndex) set level 1
					$torArb($torIndex) set link_bw [expr ($bw_torAgg/1000.0)]
					$ns makeLink $tor($torIndex) $torArb($torIndex) $bw_endhostTor $link_delay $pkSize $cbq_enable $qLimit -1
					if { $k == 0 } {
						$ns makeLink $tor($torIndex) $aggArb($aggIndex) $bw_endhostTor $link_delay $pkSize $cbq_enable $qLimit -1
					puts "AggArb $aggIndex is added under ToR $torIndex"
					}
					$ns addArbitrators $torArb($torIndex) $aggArb($aggIndex) 0 $arb_port $paseArbInvokerTor($torIndex)
				} else {
					$ns addArbitrators $tor($torIndex) $agg($aggIndex) 0 $arb_port $paseArbInvokerTor($torIndex)
				}
			}

			# Create Endhosts 
			for { set l 0 } { $l < $num_hosts } { incr l} {
				set hostIndex [expr ((($aggIndex*$num_tors)+$k)*$num_hosts)+$l]
				set host($hostIndex) [$ns node]
				if { $SRC == "TCP/CTP" } {
					$host($hostIndex) set level 0
					$host($hostIndex) set link_bw [expr ($bw_endhostTor/1000.0)]
				}

				# links between TORs -> endhosts				
				$ns makeLink $host($hostIndex) $tor($torIndex) $bw_endhostTor $link_delay $pkSize $cbq_enable $qLimit -1
				if { $SRC == "TCP/CTP" } {
					# add arbitrator agents
					set paseArbInvokerHost($hostIndex) [new Agent/TCP/PaseArbitrator]
					if { $separate_arbs == 1 } {
						$ns addArbitrators $host($hostIndex) $torArb($torIndex) 1 $arb_port $paseArbInvokerHost($hostIndex)
					} else {
						$ns addArbitrators $host($hostIndex) $tor($torIndex) 1 $arb_port $paseArbInvokerHost($hostIndex)
					}
				}
			}
		}
	}
}

# End: setup topology ------------------------------------------

# Begin: agents and sources ------------------------------------

## SETUP for LONG FTP FLOWS...
set longFlowCount 0 ; # keep this counter

for { set racks [expr 0] } { $racks < [expr ($num_tors * $num_aggs)/2] } {incr racks} {
	for {set fptor [expr 0] } {$fptor < [expr $ftpFlowPerTor]} {incr fptor}  {

		set hIndex [expr $racks * $num_hosts]
		set hostIndex [expr $hIndex + ($fptor % $num_hosts)]

		set tr_agent($longFlowCount) [new Agent/$SRC]
		set tr_agent_sink($longFlowCount) [new Agent/$SINK]

		$tr_agent_sink($longFlowCount) listen ; # ?? is it needed
		$ns attach-agent $host($hostIndex) $tr_agent($longFlowCount)
		$ns attach-agent $host([expr $hostIndex+($totalHosts/2)]) $tr_agent_sink($longFlowCount)
		
		$tr_agent($longFlowCount) set packetSize_ $pkSize
		$tr_agent($longFlowCount) set fid_ [expr $longFlowCount]
		$tr_agent_sink($longFlowCount) set fid_ [expr $longFlowCount]

		$ns connect $tr_agent($longFlowCount) $tr_agent_sink($longFlowCount)
		set ftp($longFlowCount) [new Application/FTP]
		$ftp($longFlowCount) attach-agent $tr_agent($longFlowCount)    

		$ns at 0.0 "$ftp($longFlowCount) start"
		$ns at $sim_time "$ftp($longFlowCount) stop"
		puts "Flow $longFlowCount will stop at $sim_time secs"

		set longFlowCount [expr $longFlowCount+1]
	}
}


if { $av_fsize == 50 } {
    set min_s 2000.0
    set max_s 98000.0

} elseif { $av_fsize == 100} {
    set min_s 2000.0
    set max_s 198000.0
} elseif { $av_fsize == 300} {
    set min_s 100000.0
    set max_s 500000.0
} else {
    set min_s 2000.0
    set max_s 98000.0
}

puts "avg. flow size is $av_fsize KB"

set av_file_size [expr ($min_s + $max_s) / (2 * 1000)] ; # calc in kb

set file_size [new RNG];                       # This rv is used for generating file sizes for short flows
$file_size seed 2
set short_tcp [new RandomVariable/Uniform]
$short_tcp use-rng $file_size
$short_tcp set min_ $min_s
$short_tcp set max_ $max_s

if { $simpleFlows == 1} {

	set av_inter_arrival [expr (($av_file_size*1024*8) / ($mice_load*$btnk_bw*1000000))];  
	puts "SHORT FLOWS THRU CORE: mean inter-arrival time = $av_inter_arrival";
	set short_arrival [new RNG];                              # This rv is used for generating inter-arrival times
	$short_arrival seed 2
	set s_arrival [new RandomVariable/Exponential]
	$s_arrival set avg_ $av_inter_arrival
	$s_arrival use-rng $short_arrival

	########  SHORT FLOWS GOING THRU THE CORE SWITCH

	set sink 0
	set short_flow_id 8000
	set global_time 0.0

	while {$global_time <= [expr $sim_time/2]} {


	    if { $sink == [expr $totalHosts/2] } {
			set sink 0
	    }

	    set transfer_size [expr [$short_tcp value]]
	    set short_flow_id [expr $short_flow_id + 1]

	    set stcp [build-short-lived $host($sink) $host([expr $sink+($totalHosts/2)]) $pkSize $short_flow_id $sink $global_time $SRC $SINK $transfer_size $dctcp_enable] 

	    set inter [expr [$s_arrival value]]
	    set global_time [expr $global_time + $inter]
	    set sink [expr $sink + 1]
	}

}
#### SHORT FLOWS: GOING THRU AGG SWITCHES ONLY
if {$shortFlowsInterRackThruAggs == 1} {
	set btnk_bw_level2 [expr $btnk_bw/$num_aggs]; # this expression may become incorrect if the current bottleneck is not the agg->core link

	set av_inter_arr_l2 [expr (($av_file_size*1024*8) / ($mice_load*$btnk_bw_level2*1000000))];  # 1000000 has been multiplied because bneck_bw is in Mbps
	puts "SHORT FLOWS THRU AGG: mean inter-arrival time = $av_inter_arr_l2";
	set short_arr_l2 [new RNG];                                                   # This rv is used for generating inter-arrival times
	$short_arr_l2 seed 3
	set s_arr [new RandomVariable/Exponential]
	$s_arr set avg_ $av_inter_arr_l2
	$s_arr use-rng $short_arr_l2

	set sink 0
	set hostsUnderAgg [expr $num_hosts*$num_tors]

	for { set aggInd 0 } { $aggInd < [expr $num_cores * $num_aggs] } { incr aggInd } {
		set sink [expr $aggInd*$hostsUnderAgg]
		set global_time 0.0
		set h 0
		while {$global_time <= [expr $sim_time/2]} {
			set srcIndex [expr $sink + [expr $h % ($hostsUnderAgg/2)]]
			set destIndex [expr $srcIndex +($hostsUnderAgg/2)]
			set transfer_size [expr [$short_tcp value]]
			set short_flow_id [expr $short_flow_id + 1]

			set stcp [build-short-lived $host($srcIndex) $host($destIndex) $pkSize $short_flow_id $srcIndex $global_time $SRC $SINK $transfer_size $dctcp_enable]
			if { $SRC == "TCP/CTP" } { 
				$stcp set level 2
			}

			set inter_time [expr [$s_arr value]]
			set global_time [expr $global_time + $inter_time]
			set h [expr $h + 1]    
		}
	}
}
########################################################


## All to All short flows

if {$AlltoAllFlows == 1} {

	set no_endhosts $num_tors*$num_aggs*$num_hosts
	set av_inter_arrival [expr (($av_file_size*1024*8) / ($mice_load*$btnk_bw*1000000*2))];  
 
	puts "SHORT FLOWS THRU CORE: mean inter-arrival time = $av_inter_arrival";
	
	set short_arrival [new RNG];                                                   # This rv is used for generating inter-arrival times
	$short_arrival seed 2
	set s_arrival [new RandomVariable/Exponential]
	$s_arrival set avg_ $av_inter_arrival
	$s_arrival use-rng $short_arrival

	set rng2 [new RNG]; 
	$rng2 seed 2
	set index [new RandomVariable/Uniform]
	$index use-rng $rng2
	$index set min_ 0
	$index set max_ [expr $no_endhosts-1]
	set sink 0
	set short_flow_id 8000
	set global_time 0.0

	while {$global_time <= [expr $sim_time/2]} {

	if { $sink == [expr $totalHosts/2] } {
		set sink 0
	}

	set src_ind [expr round([expr [$index value]])]
	set dst_ind [expr round([expr [$index value]])]
	while { $src_ind == $dst_ind } {
		set dst_ind [expr round([expr [$index value]])]
	}


	set transfer_size [expr [$short_tcp value]]
	set short_flow_id [expr $short_flow_id + 1]

	set stcp [build-short-lived $host($src_ind) $host($dst_ind) $pkSize $short_flow_id $sink $global_time $SRC $SINK $transfer_size $dctcp_enable] 

	$stcp set level [flowLevel $num_hosts $num_tors $src_ind $dst_ind]

	set inter [expr [$s_arrival value]]

	set global_time [expr $global_time + $inter]

	set sink [expr $sink + 1]
}

}
# End: agents and sources --------------------------------------

if {$cbq_enable==1 && $getQmonQueueLevelStats==1} {
	$ns at [expr $STATS_START + $STATS_INTR] "record"
}

# Statistics
set Out [open Out.ns w]

Agent/$SRC instproc done {} {
	global tcp ptcp rtcp stcp rstcp ptcp rptcp flows_n ns s_arrival arrival_t short_tcp Out ftp SRC
	set duration [expr [$ns now] - [$self set starts]]
	puts $Out "[$self set node] \t [$self set sess] \t [$self set starts] \t\
		   [$ns now] \t $duration \t [$self set ndatapack_] \t\
		   [$self set ndatabytes_] \t [$self set nrexmitbytes_] \t\
		   [expr [$self set ndatabytes_]/$duration] \t\
		   [$self set ncwndcuts1_] \t [$self set nrexmit_]\t "
	if { $SRC == "TCP/CTP" } {
		set level_ [$self set level]
	}
}
# Monitoring code

puts "\n \t\t\t-----   MONITORING SETUP   -----\n"


if {$getQmonLinkLevelStats == 1} {

	for { set i 0 } { $i < $num_cores } { incr i } {
		for { set j 0 } { $j < $num_aggs } { incr j } {
			set aggIndex [expr ($i*$num_aggs)+$j] 

			set qmon_ab($aggIndex) [$ns monitor-queue $agg($aggIndex) $core($i) ""]
			set bing_ab($aggIndex) [$qmon_ab($aggIndex) get-bytes-integrator];	# bytes integrator 
			set ping_ab($aggIndex) [$qmon_ab($aggIndex) get-pkts-integrator];	    # packets integrator

			set fileq($aggIndex) "qmon.trace"
			set futil_name($aggIndex) "qmon.util"
			set floss_name($aggIndex) "qmon.loss"
			set fqueue_name($aggIndex) "qmon.queue"

			append fileq($aggIndex) "Agg$aggIndex"
			append fileq($aggIndex) "Core$i"
			append futil_name($aggIndex) "Agg$aggIndex"
			append futil_name($aggIndex) "Core$i"
			append floss_name($aggIndex) "Agg$aggIndex"
			append floss_name($aggIndex) "Core$i"
			append fqueue_name($aggIndex) "Agg$aggIndex"
			append fqueue_name($aggIndex) "Core$i"

			set fq_mon($aggIndex) [open $fileq($aggIndex) w]
			set f_util($aggIndex) [open $futil_name($aggIndex) w]
			set f_loss($aggIndex) [open $floss_name($aggIndex) w]
			set f_queue($aggIndex) [open $fqueue_name($aggIndex) w]

			$ns at $STATS_START  "$qmon_ab($aggIndex) reset"
			$ns at $STATS_START  "$bing_ab($aggIndex) reset"
			$ns at $STATS_START  "$ping_ab($aggIndex) reset"
			$ns at [expr $STATS_START+$STATS_INTR] "linkDump [$ns link $agg($aggIndex) $core($i)] $bing_ab($aggIndex) $ping_ab($aggIndex) $qmon_ab($aggIndex) $STATS_INTR A-B $fq_mon($aggIndex) $f_util($aggIndex) $f_loss($aggIndex) $f_queue($aggIndex) [expr $qLimit*$pkSize]" ; #last one $buf_bytes
	#		}
		}
	}
}

proc curr_time {} {
	global ns
	set now [$ns now]
	puts "Current Time: $now"
}
for { set i 0 } { $i < $sim_time } { incr i } {
	$ns at $i "curr_time"
}
$ns at $sim_time "finish"

#Run the simulation
$ns run

