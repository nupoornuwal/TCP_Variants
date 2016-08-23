#Create a simulator object
set ns [new Simulator]

#Define different colors for data flows (for NAM)
$ns color 1 Blue
#$ns color 2 Red
$ns color 2 Green

#set TCP variant1
set variant1 [lindex $argv 0]
#set TCP variant2
set variant2 [lindex $argv 1]
#Set CBR RATE
set rate [lindex $argv 2]
#Open the NAM trace file
#set nf [open testvinay.nam w]
#puts $variant1
#puts $variant2
set tf [open testvinay${variant1}_${variant2}${rate}.tr w]
#$ns namtrace-all $nf
$ns trace-all $tf 
#Define a 'finish' procedure
proc finish {} {
        global ns nf tf
        $ns flush-trace
        #Close the NAM trace file
        #close $nf
	close $tf
        #Execute NAM on the trace file
        #exec nam testvinay.nam &
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

if {$variant1 eq "Reno"} {
        set tcp1 [new Agent/TCP/Reno]
} elseif {$variant1 eq "NewReno"} {
        set tcp1 [new Agent/TCP/Newreno]
} elseif {$variant1 eq "Vegas"} {
        set tcp1 [new Agent/TCP/Vegas]
}


#Setup a TCP connection
$tcp1 set class_ 1
$ns attach-agent $n0 $tcp1
set sink2 [new Agent/TCPSink]
$ns attach-agent $n4 $sink2
$ns connect $tcp1 $sink2
$tcp1 set fid_ 1

#Setup a FTP over TCP connection
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp1 set type_ FTP

#SET TCP2 flow

if {$variant2 eq "Reno"} {
        set tcp2 [new Agent/TCP/Reno]
} elseif {$variant2 eq "Vegas"} {
        set tcp2 [new Agent/TCP/Vegas]
}

#Setup 2nd TCP connection
#set tcp [new Agent/TCP/Reno]
$tcp2 set class_ 2
$ns attach-agent $n1 $tcp2
set sink1 [new Agent/TCPSink]
$ns attach-agent $n5 $sink1
$ns connect $tcp2 $sink1
$tcp2 set fid_ 2
#$tcp set rate_ 30mb

#Setup 2ND FTP over TCP connection
set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2
$ftp2 set type_ FTP


#Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n2 $udp
set sink [new Agent/UDP]
$ns attach-agent $n3 $sink
$ns connect $udp $sink
#$udp set fid_ 2

#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ ${rate}mb
$cbr set random_ false


#Schedule events for the CBR and FTP agents
$ns at 20.0 "$cbr start"
$ns at 0.0 "$ftp1 start"
$ns at 0.0 "$ftp2 start"
$ns at 30.0 "$cbr stop"
$ns at 30.0 "$ftp1 stop"
$ns at 30.0 "$ftp2 stop"
#Detach tcp and sink agents (not really necessary)
#$ns at 5.0 "$ns detach-agent $n0 $tcp ; $ns detach-agent $n4 $sink"
#$ns at 5.0 "$ns detach-agent $n1 $tcp ; $ns detach-agent $n5 $sink"

#Call the finish procedure after 5 seconds of simulation time
$ns at 30.0 "finish"

#Print CBR packet size and interval
#puts "CBR packet size = [$cbr set packet_size_]"
#puts "CBR interval = [$cbr set interval_]"

#Run the simulation
$ns run

