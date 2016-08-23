#Create a simulator object
set ns [new Simulator]

#Define different colors for data flows (for NAM)
$ns color 1 Blue
$ns color 2 Red
#set TCP variant
set variant [lindex $argv 0]
#Set CBR RATE
set rate [lindex $argv 1]

#Open the NAM trace file
#set nf [open testnupoor.nam w]
set tf [open testnupoor${variant}${rate}.tr w]
#$ns namtrace-all 
$ns trace-all $tf 
#Define a 'finish' procedure
proc finish {} {
        global ns nf tf
        $ns flush-trace
        #Close the NAM trace file
        #close $nf
	close $tf
        exit 0
}

#Create four nodes
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
#Create links between the nodes
$ns duplex-link $n0 $n2 10Mb 10ms DropTail
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n4 $n3 10Mb 10ms DropTail
$ns duplex-link $n5 $n3 10Mb 10ms DropTail
#Set Queue Size of link (n2-n3) to 10
$ns queue-limit $n2 $n3 10

#Give node position (for NAM)
$ns duplex-link-op $n0 $n2 orient right-down
$ns duplex-link-op $n1 $n2 orient right-up
$ns duplex-link-op $n2 $n3 orient right
$ns duplex-link-op $n4 $n3 orient left-down
$ns duplex-link-op $n5 $n3 orient left-up
#Monitor the queue for link (n2-n3). (for NAM)
$ns duplex-link-op $n2 $n3 queuePos 0.5

#puts $variant
#Setup a TCP connection
if {$variant eq "Tahoe"} {
        set tcp [new Agent/TCP]
} elseif {$variant eq "Reno"} {
        set tcp [new Agent/TCP/Reno]
} elseif {$variant eq "NewReno"} {
        set tcp [new Agent/TCP/Newreno]
} elseif {$variant eq "Vegas"} {
        set tcp [new Agent/TCP/Vegas]
}

#set tcp [new Agent/TCP]
$tcp set class_ 2
$ns attach-agent $n0 $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink
$ns connect $tcp $sink
$tcp set fid_ 1

#Setup a FTP over TCP connection
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP


#Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n2 $udp
set sink [new Agent/UDP]
$ns attach-agent $n3 $sink
$ns connect $udp $sink
$udp set fid_ 2

#Setup a CBR over UDP connection
#set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ ${rate}mb
$cbr set random_ false

#Schedule events for the CBR and FTP agents
$ns at 3.0 "$cbr start"
$ns at 0.0 "$ftp start"
$ns at 20.0 "$ftp stop"
$ns at 15.0 "$cbr stop"

#Detach tcp and sink agents (not really necessary)
#$ns at 2.0 "$ns detach-agent $n0 $tcp ; $ns detach-agent $n4 $sink"

#Call the finish procedure after 5 seconds of simulation time
$ns at 15.0 "finish"

#Print CBR packet size and interval
#puts "CBR packet size = [$cbr set packet_size_]"
#puts "CBR interval = [$cbr set interval_]"

#Run the simulation
$ns run

