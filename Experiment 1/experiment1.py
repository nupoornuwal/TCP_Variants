import subprocess
import os  
import sys
from operator import sub
#from numphy import *
ns_command= "/course/cs4700f12/ns-allinone-2.35/bin/"

variant= ['Tahoe','Reno','NewReno','Vegas']
global throughtput
global start
for i in variant:
	for rate in range(1,15):
		os.system("cd " +ns_command)
                os.system('ns '+'test.tcl '+i+' '+str(rate))			  		

def throughtput(var,rate):
	file="testnupoor" + i + str(rate) +".tr"
	#print file
	f=open(file)
	lines=f.readlines()
	#print lines
	f.close()
	received_packet=0
	start_received_time=10.0
	end_time=0.0
	for k in lines:
		#print k
		n=k.split()
		if n[7]=="1":
			if n[0]=="r" and n[2]=="0" and n[10]=="0":
                        		#if float(n[1])<received_time:
                                		start_received_time=float(n[1])
                                		#print 'received_time', received_time

			if n[0]== "r" and  n[3]== "4" and n[4]== "tcp" :
					received_packet=received_packet+int(n[5])
					end_time=float(n[1])
					#print end_time,type(end_time)
	
	#print 'end_time',end_time
	#print 'received_time',start_received_time
	time=(end_time-start_received_time)*1000000
	#print 'time',time
	#thoughput=received_packet*8/(float(time))
	#print 'throughput',throughput
	return received_packet*8/(float(time))


def latency(var,rate):
	file="testnupoor" + i + str(rate) +".tr"
        print file
        f=open(file)
        lines=f.readlines()
        #print lines
        f.close()
	count=0
	highest_id =0
	seq_num=[]
	start_time=[]
	end_seq_num=[]
	latency_seq_time=[]
	duration=[]
	for k in lines:
                #print k
                n=k.split()
		#print n[10]
		if n[0]=="+" and n[2]=="0" and  n[4]=="tcp":
			a=n[10]
			if a not in seq_num:
				seq_num.append(a)
				#print 'seq_num',seq_num,'len',len(seq_num)
				#print 'len',len(seq_num)
				start_time.append(n[1])
				#print 'len start',len(start_time)
		if n[0]=="r" and n[3]=="4" and n[4]=="tcp":
				b=n[10]
				end_seq_num.append(b)
				#print 'end_seq_num',end_seq_num,'len',len(end_seq_num)
				#print 'endlen',len(end_seq_num)
				latency_seq_time.append(n[1]) 
				#print'end', len(latency_seq_time)
	length=len(start_time)-len(latency_seq_time)
	for k in range(length):
		start_time.pop()	
	#print len(start_time)==len(latency_seq_time)
	for k in range(len(start_time)):
		duration.append(float(latency_seq_time[k])-float(start_time[k]))
	#latency_average=sum(duration)/len(duration)
	return sum(duration)/len(duration)	


def droprate(var,rate):
	file="testnupoor" + i + str(rate) +".tr"
        #print file
        f=open(file)
        lines=f.readlines()
        #print lines
        f.close()
	packet_send=0
	packet_received=0
	for k in lines:
                #print k
                n=k.split()
		if n[7]=="1":
			if n[0]=="+" and n[2]=="0":
				packet_send += 1
			if n[0]=="r" and n[3]=="4":
				packet_received += 1
				
    	if packet_send == 0:
    		return 0
	else:
		drop_rate=(float(packet_send-packet_received)/float(packet_send))*100
		return drop_rate				

def RTT(var,rate):
	file="testnupoor" + i + str(rate) +".tr"
        #print file
        f=open(file)
        lines=f.readlines()
        #print lines
        f.close()
        highest_id =0
        RTT_start_seqnum=[]
        RTT_start_time=[]
	rtt_list=[]
      	start_tup=()
	c=[]
        for k in lines:
                #print k
                n=k.split()
                #print n[10]
		if n[7]=='1':
               		 if n[0]=="+" and n[2]=="0" and  n[4]=="tcp":
				if n[10] not in RTT_start_seqnum:
					RTT_start_seqnum.append(n[10]) 
                                	start_tup=(n[10],n[1])
                                	c.append(start_tup)
                                
                if n[0]=="r" and n[3]=="0" and n[4]=="ack":
                                b=n[10]
                                for tup in c:
					#print "tuple",tup
                                        if n[10] in tup:
                                                        RTT_start_time=float(tup[1])
                                                        rtt= float(n[1])-RTT_start_time
                                                        rtt_list.append(rtt)
        #print 'rttlist', rtt_list
	average_rtt=sum(rtt_list)/len(rtt_list)
        return  average_rtt
									

#########################


j=1
file1=open("exp1.xls","w")
file1.write("\tTahoe\tReno\tnewreno\tVegas\n")
file2=open("exp2.xls","w")
file2.write("\tTahoe\tReno\tnewreno\tVegas\n")
file3=open("exp3.xls","w")
file3.write("\tTahoe\tReno\tnewreno\tVegas\n")
file4=open("exp4.xls","w")
file4.write("\tTahoe\tReno\tnewreno\tVegas\n")

for rate in range(1,15):
       str_throughput=''
       str_latency=''
       str_droprate=''
       str_RTT=''
       file1.write("%d\t"%j)
       file2.write("%d\t"%j)
       file3.write("%d\t"%j)
       file4.write("%d\t"%j)
       for i in variant:
    		str_throughput=str(throughtput(i,rate))+"\t"
    		file1.write("%s"%( str_throughput))
		
		str_latency=str(latency(i,rate))+"\t"
		file2.write("%s"%(str_latency))
		
		str_droprate=str(droprate(i,rate))+"\t"
		file3.write("%s"%(str_droprate))
		
		str_RTT=str(RTT(i,rate))+"\t"
		file4.write("%s"%(str_RTT))    
       j=j+1	
       file1.write("\n")
       file2.write("\n")
       file3.write("\n")
       file4.write("\n")
	
file1.close()
file2.close()
file3.close()
file4.close()

