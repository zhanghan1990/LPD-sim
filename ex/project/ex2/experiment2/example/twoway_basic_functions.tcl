

#procedure to compute average queue length 
#proc queueLength {sum number file} { 
#    global ns qmonitor 
#    set time 0.1 
#    set len [$qmonitor set pkts_] 
#    set now [$ns now] 
#    set sum [expr $sum+$len] 
#    set number [expr $number+1] 
#    #write the average queue length in to a file 
#    puts $file "[expr $now+$time] [expr 1.0*$sum/$number]" 
#    $ns at [expr $now+$time] "queueLength $sum $number $file" 
#} 
#$ns at 0 "queueLength 0 0 $avgf"


#
# Print periodic "i'am alive" message
#
proc print_time {interval} {
global ns 
        #puts stdout [format "\nTime: %.2f" [$ns now]]
        $ns at [expr [$ns now]+$interval] "print_time $interval"
}


#
# Dump the statistics of a (unidirectional) link periodically 
#
proc linkDump {link binteg pinteg qmon interval name linkfile util loss queue buf_bytes} {
global ns
        set now_time [$ns now]
        $ns at [expr $now_time + $interval] "linkDump $link $binteg $pinteg $qmon $interval $name $linkfile $util $loss $queue $buf_bytes"
        set bandw [[$link link] set bandwidth_]
        set queue_bd [$binteg set sum_]
        set abd_queue [expr $queue_bd/[expr 1.*$interval]]
        set queue_pd [$pinteg set sum_]
        set apd_queue [expr $queue_pd/[expr 1.*$interval]]
        set utilz [expr 8*[$qmon set bdepartures_]/[expr 1.*$interval*$bandw]]    

        if {[$qmon set parrivals_] != 0} {
                set drprt [expr [$qmon set pdrops_]/[expr 1.*[$qmon set parrivals_]]]
        } else {
                set drprt 0
        }
	if {$utilz != 0} {;	# compute avg queueing delay based on Little's formula
		set a_delay [expr ($abd_queue*8*1000)/($utilz*$bandw)]
	} else {
		set a_delay 0.
	}
#        puts stdout [format "\nTime interval: %.2f-%.2f" [expr [$ns now] - $interval] [$ns now]]
        puts $linkfile [format "\nTime interval: %.5f-%.5f" [expr [$ns now] - $interval] [$ns now]]
        puts $linkfile [format "Link %s: Utiliz=%.3f LossRate=%.3f AvgDelay=%.2fms AvgQueue(P)=%.2f AvgQueue(B)=%.0f" $name $utilz $drprt $a_delay $apd_queue $abd_queue]
    
        #loss_sample, util_sample and queue_sample
    
    

        set av_qsize [expr [expr $abd_queue * 100] / $buf_bytes]
        set utilz [expr $utilz * 100]
        set drprt [expr $drprt * 100]

    set buf_pkts [expr $buf_bytes / 1000]

#        puts "Buffer Size (bytes) = $buf_bytes"
#        puts "Buffer Size (pkts) = $buf_pkts"

        puts $util [format "%.5f   %.3f" [$ns now] $utilz]
	puts $loss [format "%.5f   %.3f" [$ns now] $drprt]
	puts $queue [format "%.5f   %.3f" [$ns now] $apd_queue]
#	puts $queue [format "%.5f   %.3f" [$ns now] $av_qsize]

    
        $binteg reset
        $pinteg reset
        $qmon reset
}


#
# Print the statistics of a flow
#
proc printFlow {f outfile fm interval} {
global ns 
#puts $outfile [format "FID: %d pckarv: %d bytarv: %d pckdrp: %d bytdrp: %d rate: %.0f drprt: %.3f" [$f set flowid_] [$f set parrivals_] [$f set barrivals_] [$f set pdrops_] [$f set bdrops_] [expr [$f set barrivals_]*8/($interval*1000.)] [expr [$f set pdrops_]/double([$f set parrivals_])] ]

# flow_id, rate and drprt,
#puts $outfile [format "%d %.0f  %.3f" [$f set flowid_] [expr [$f set barrivals_]*8/($interval*1000000.)] [expr [$f set pdrops_]/double([$f set parrivals_])] ]

puts $outfile [format "%d %.6f " [$f set flowid_] [expr [$f set barrivals_]*8/($interval*1000000.)] ]


####

set number 30
for {set a 0} { $a < $number} {incr a} {
	set fl "flow"
	append fl $a
	set flow($a) [open $fl a]

	if { [$f set flowid_] == $a } {
		puts $flow($a) [format "%.4f %.6f" [$ns now] [expr [$f set barrivals_]*8/($interval*1000000.)] ]
	}
	close $flow($a)
}

####

}


#
# Dump the statistics of all flows
#
proc flowDump {link fm file_p interval} {
global ns 

    $ns at [expr [$ns now] + $interval]  "flowDump $link $fm $file_p $interval"
        puts $file_p [format "\nTime: %.2f" [$ns now]] 
        set theflows [$fm flows]
        if {[llength $theflows] == 0} {
                return
        } else {
        	set total_arr [expr double([$fm set barrivals_])]
        	if {$total_arr > 0} {
                	foreach f $theflows {
                        	set arr [expr [expr double([$f set barrivals_])] / $total_arr]
                        	if {$arr >= 0.0001} {
				    printFlow $f $file_p $fm $interval
                        	}       
                        	$f reset
                	}       
                	$fm reset
        	}
        }
}



#
# Create "infinite-duration" FTP connection
#
proc inf_ftp {id src dst maxwin pksize starttm} {
global ns 
	set tcp [$ns create-connection TCP/Newreno $src TCPSink/DelAck $dst $id]
	set ftp [$tcp attach-source FTP]
  	$tcp set window_ 	$maxwin
  	$tcp set packetSize_ 	$pksize
	$ns at $starttm "$ftp start"
	return $tcp
}


#
# Create an Exponential On-Off source
#
proc build-exp-off { src dest pktSize burstTime idleTime rate id startTime } {
    global ns
    set cbr [new Agent/CBR/UDP]
    $ns attach-agent $src $cbr
    set null [new Agent/Null]
    $ns attach-agent $dest $null
    $ns connect $cbr $null
    set exp1 [new Traffic/Expoo]
    $exp1 set packet-size $pktSize
    $exp1 set burst-time  [expr $burstTime / 1000.0] 
    $exp1 set idle-time   [expr $idleTime / 1000.0]
    $exp1 set rate        [expr $rate * 1000.0]
    $cbr  attach-traffic  $exp1
    $ns at $startTime "$cbr start"
    $cbr set fid_      $id
    return $cbr
}


#
# Create Short-lived TCP flows
#
proc build-short-lived { src dest pktSize fid node_id startTime tcp_src tcp_sink transfer_size dctcp} {
    global ns

	#set tcp [$ns create-connection $tcp_src $src $tcp_sink $dest fid]
	set tcp [new Agent/$tcp_src]
	set sink [new Agent/$tcp_sink]
	if {$dctcp} {
		$sink listen
	}
	$ns attach-agent $src $tcp
	$ns attach-agent $dest $sink
	$sink set fid_ fid
	$ns connect $tcp $sink
	#$tcp set window_ 10000
	$tcp set fid_ $fid
	set ftp [$tcp attach-source FTP]

	$tcp set starts $startTime
	$tcp set sess $fid
	$tcp set node $node_id
	$tcp set packetSize_ $pktSize
	$tcp set size $transfer_size
	$tcp set flow_size [expr $transfer_size/1024]

	$ns at [$tcp set starts] "$ftp send [$tcp set size]"
	return $tcp
}

proc flowLevel { num_hosts num_tors src_ind dst_ind } {

	if { $src_ind/$num_hosts == $dst_ind/$num_hosts } {
		return 1
	} elseif { $src_ind/($num_hosts*$num_tors) == $dst_ind/($num_hosts*$num_tors) } {
		return 2
	} else {
		return 3
	}
}
