import subprocess
import os  
import sys
from operator import sub
#from numphy import *
ns_command= "/course/cs4700f12/ns-allinone-2.35/bin/"

variant= ['Reno_Reno','NewReno_Reno','Vegas_Vegas','NewReno_Vegas']
global throughtput
global start
 
def throughtput(var,rate):
	global thoughtput
	file='test'+i+str(rate)+'.tr'
	#print 'FILE', file
	f=open(file)
	lines=f.readlines()
	#print lines
	f.close()
	received_packet1=0
	received_packet2=0
	start_received_time1=10.0
	start_received_time2=10.0
	end_time1=0.0
	end_time2=0.0
	for k in lines:
		#print k
		n=k.split()
		if n[7]=="1":
			if n[0]=="r" and n[2]=="0" and n[10]=="0":
                        		#if float(n[1])<received_time:
                                		start_received_time1=float(n[1])
                                		#print 'received_time1', start_received_time1

			if n[0]== "r" and  n[3]== "4" and n[4]=="tcp" :
					received_packet1=received_packet1+int(n[5])
					end_time1=float(n[1])
					#print end_time1,type(end_time1)
		if n[7]=="2":
			if n[0]=="r" and n[2]=="1" and n[10]=="0":
                                        #if float(n[1])<received_time:
                                                start_received_time2=float(n[1])
                                                #print 'received_time', start_received_time2

                        if n[0]== "r" and  n[3]== "5" and n[4]== "tcp" :
                                        received_packet2=received_packet2+int(n[5])
                                        end_time2=float(n[1])
                                        #print 'end_time2',end_time2
			
	
	#print 'end_time1',end_time1
	#print 'received_time1',start_received_time1
	#print 'end_time2',end_time2
        #print 'received_time2',start_received_time2
	time1=(end_time1-start_received_time1)*1000000
	#print 'time',time1
	thoughput1=received_packet1*8/(float(time1))
	#print 'throughput',throughput1
	time2=(end_time2-start_received_time2)*1000000
	throughput2=received_packet2*8/(float(time2))	
	return str(thoughput1) + '\t' + str(throughput2)


def latency(var,rate):
        file='test'+i+str(rate)+'.tr'
        print file
        f=open(file)
        lines=f.readlines()
        #print lines
        f.close()
        count=0
	count1=0
        highest_id =0
	highes_id1=0
        start_tup=()
	start_tup1=()
        end_tup=[]
	end_tup1=[]
        start_time=0
	start_time1=0
        c=[]
	c1=[]
        latency_list=[]
	latency_list1=[]
        seq_num=[]
	seq_num1=[]
	for k in lines:
             #print k
             n=k.split()
             if n[7]=='1':
                if n[0]=="+" and n[2]=="0" and  n[4]=="tcp":
			if n[10] not in seq_num:     #check for retransmission
				seq_num.append(n[10]) 
                                start_tup=(n[10],n[1])
                                c.append(start_tup)
                if n[0]=="r" and n[3]=="4" and n[4]=="tcp":
                                b=n[10]
                                for tup in c:
					#print "tuple",tup
                                        if n[10] in tup:
                                                        start_time=float(tup[1])
                                                        latency= float(n[1])-start_time
                                                        latency_list.append(latency)
	     if n[7]=='2':
                if n[0]=="+" and n[2]=="1" and  n[4]=="tcp":
                        if n[10] not in seq_num1:
                                seq_num1.append(n[10])
                                start_tup1=(n[10],n[1])
                                c1.append(start_tup1)
                if n[0]=="r" and n[3]=="5" and n[4]=="tcp":
                                b=n[10]
                                for tup in c1:
                                        #print "tuple",tup
                                        if n[10] in tup:
                                                        start_time1=float(tup[1])
                                                        latency1= float(n[1])-start_time1
                                                        latency_list1.append(latency1)
							#print 'latency_list1', latency_list1, len(latency_list1)         
       
	print 'latency_list1',len(latency_list1)
	print 'latency_list',len(latency_list)
        average_latency=sum(latency_list)/len(latency_list)
	average_latency1=sum(latency_list1)/len(latency_list1)
        #print 'AverageLatency:', average_latency 
	return str(average_latency1) + '\t' + str(average_latency1)

def droprate(var,rate):
	file='test'+i+str(rate)+'.tr'
        #print 'FILE',file
        f=open(file)
        lines=f.readlines()
        #print lines
        f.close()
	packet_send1=0
	packet_received1=0
	packet_send2=0
	packet_received2=0
	for k in lines:
                #print k
                n=k.split()
		if n[7]=="1":
			if n[0]=="+" and n[2]=="0":
				packet_send1 += 1
			  	#print 'Packet_send1',packet_send1
			if n[0]=="r" and n[3]=="4":
				packet_received1 += 1
				#print 'Packet_received1',packet_received1
		if n[7]=="2":
			if n[0]=="+" and n[2]=="1":
				packet_send2 +=1
				#print 'Packet_send2',packet_send2
			if n[0]=="r" and n[3]=="5":
				packet_received2 +=1
				#print 'Packet_received2',packet_received2
	#print 'Packet_send1',packet_send1
	#print 'Packet_received1',packet_received1
	#print 'Packet_send2',packet_send2
        #print 'Packet_received2',packet_received2
							
    	if packet_send1 == 0:
    		return 0
	else:
		drop_rate1=(float(packet_send1-packet_received1)/float(packet_send1))*100
		#print 'drop_rate1',drop_rate1
	if packet_send2 == 0:
		return 0
	else:
		drop_rate2=(float(packet_send2-packet_received2)/float(packet_send2))*100
		#print 'drop_rate2',drop_rate2
	return str(drop_rate1) + '\t' + str(drop_rate2)

def RTT(var,rate):
        file='test'+i+str(rate)+'.tr'
        #print file
        f=open(file)
        lines=f.readlines()
        #print lines
        f.close()
        RTT_count=0
	RTT_count1=0
        RTT_start_tup=()
	RTT_start_tup1=()
        RTT_start_time=0
	RTT_start_time1=0
        RTT_c=[]
	RTT_c1=[]
        RTT_list=[]
	RTT_list1=[]
        RTT_seq_num=[]
	RTT_seq_num1=[]
	for k in lines:
             #print k
             n=k.split()
             if n[7]=='1':
                if n[0]=="+" and n[2]=="0" and  n[4]=="tcp":
			if n[10] not in RTT_seq_num:
				RTT_seq_num.append(n[10]) 
                                RTT_start_tup=(n[10],n[1])
                                RTT_c.append(RTT_start_tup)
                if n[0]=="r" and n[3]=="0" and n[4]=="ack":
                                b=n[10]
                                for tup in RTT_c:
					#print "tuple",tup
                                        if n[10] in tup:
                                                        RTT_start_time=float(tup[1])
                                                        RTT= float(n[1])-RTT_start_time
                                                        RTT_list.append(RTT)
	     if n[7]=='2':
                if n[0]=="+" and n[2]=="1" and  n[4]=="tcp":
                        if n[10] not in RTT_seq_num1:
                                RTT_seq_num1.append(n[10])
                                RTT_start_tup1=(n[10],n[1])
                                RTT_c1.append(RTT_start_tup1)
                if n[0]=="r" and n[3]=="1" and n[4]=="ack":
                          b=n[10]
                          for tup in RTT_c1:
                                   #print "tuple",tup
                                   if n[10] in tup:
                                            RTT_start_time1=float(tup[1])
                                            RTT_1= float(n[1])-RTT_start_time1
                                            RTT_list1.append(RTT_1)
        #print 'RTTlist', RTT_list
	#print 'RTTLIST1',RTT_list1
	average_RTT=sum(RTT_list)/len(RTT_list)
	average_RTT1=sum(RTT_list1)/len(RTT_list1)
        #print 'AverageRTT:', average_RTT	
	#print 'AverageRTT1:',average_RTT1		
	return str(average_RTT) + '\t' + str(average_RTT1)		


for i in variant:
        for rate in range(1,10):
                tcp_split=i.split('_')
                os.system("cd " +ns_command)
                os.system('ns '+'test.tcl '+tcp_split[0]+' ' +tcp_split[1]+' '+str(rate))


j=1
file11=open("Reno_Reno_throughput.xls","w")
file11.write("\tReno\tReno\n")
file12=open("NewReno_Reno_throughput.xls","w")
file12.write("\tNewReno\tReno\n")
file13=open("Vegas_Vegas_throughput.xls","w")
file13.write("\tVegas\tVegas\n")
file14=open("NewReno_Vegas_throughput.xls","w")
file14.write("\tNewReno\tVegas\n")

file21=open("Reno_Reno_droprate.xls","w")
file21.write("\tReno\tReno\n")
file22=open("NewReno_Reno_droprate.xls","w")
file22.write("\tNewReno\tReno\n")
file23=open("Vegas_Vegas_droprate.xls","w")
file23.write("\tVegas\tVegas\n")
file24=open("NewReno_Vegas_droprate.xls","w")
file24.write("\tNewReno\tVegas\n")

file31=open("Reno_Reno_latency.xls","w")
file31.write("\tReno\tReno\n")
file32=open("NewReno_Reno_latency.xls","w")
file32.write("\tNewReno\tReno\n")
file33=open("Vegas_Vegas_latency.xls","w")
file33.write("\tVegas\tVegas\n")
file34=open("NewReno_Vegas_latency.xls","w")
file34.write("\tNewReno\tVegas\n")

file41=open("Reno_Reno_RTT.xls","w")
file41.write("\tReno\tReno\n")
file42=open("NewReno_Reno_RTT.xls","w")
file42.write("\tNewReno\tReno\n")
file43=open("Vegas_Vegas_RTT.xls","w")
file43.write("\tVegas\tVegas\n")
file44=open("NewReno_Vegas_RTT.xls","w")
file44.write("\tNewReno\tVegas\n")

for rate in range(1,10):
	str_throughput=''
	str_latency=''
	str_droprate=''
	str_RTT=''
	file11.write("%d\t"%j)
	file12.write("%d\t"%j)
	file13.write("%d\t"%j)
	file14.write("%d\t"%j)
	file21.write("%d\t"%j)
	file22.write("%d\t"%j)
	file23.write("%d\t"%j)
	file24.write("%d\t"%j)
	file31.write("%d\t"%j)
        file32.write("%d\t"%j)
        file33.write("%d\t"%j)
        file34.write("%d\t"%j)
	file41.write("%d\t"%j)
        file42.write("%d\t"%j)
        file43.write("%d\t"%j)
        file44.write("%d\t"%j)
  	for i in variant:
		if i =="Reno_Reno":
    			str_throughput=throughtput(i,rate)+"\t"
    			file11.write("%s"%( str_throughput))
			str_droprate=droprate(i,rate)
			file21.write("%s"%( str_droprate))
			str_latency=latency(i,rate)+"\t"
			file31.write("%s"%( str_latency))
			str_RTT=RTT(i,rate)+"\t"
			file41.write("%s"%( str_RTT)) 
		if i=="NewReno_Reno":
			str_throughput=throughtput(i,rate)+"\t"
                	file12.write("%s"%( str_throughput))
			str_droprate=droprate(i,rate)
                        file22.write("%s"%( str_droprate))
			str_latency=latency(i,rate)+"\t"
                        file32.write("%s"%( str_latency))
			str_RTT=RTT(i,rate)+"\t"
                        file42.write("%s"%( str_RTT))
		if i=="Vegas_Vegas":
			str_throughput=throughtput(i,rate)+"\t"
                	file13.write("%s"%( str_throughput))
			str_droprate=droprate(i,rate)
                        file23.write("%s"%( str_droprate))
			str_latency=latency(i,rate)+"\t"
                        file33.write("%s"%( str_latency))
			str_RTT=RTT(i,rate)+"\t"
                        file43.write("%s"%( str_RTT))
		if i=="NewReno_Vegas":
                	str_throughput=throughtput(i,rate)+"\t"
                	file14.write("%s"%( str_throughput))
			str_droprate=droprate(i,rate)
                        file24.write("%s"%( str_droprate))
			str_latency=latency(i,rate)+"\t"
                        file34.write("%s"%( str_latency))
			str_RTT=RTT(i,rate)+"\t"
                        file44.write("%s"%( str_RTT))
	j=j+1	
	file11.write("\n")
	file12.write("\n")
    	file13.write("\n")
	file14.write("\n")
	file21.write("\n")
	file22.write("\n")
	file23.write("\n")
	file24.write("\n")
	file31.write("\n")
        file32.write("\n")
        file33.write("\n")
        file34.write("\n")
	file41.write("\n")
        file42.write("\n")
        file43.write("\n")
        file44.write("\n")
file11.close()
file12.close()
file13.close()
file14.close()
file21.close()
file22.close()
file23.close()
file24.close()
file31.close()
file32.close()
file33.close()
file34.close()
file41.close()
file42.close()
file43.close()
file44.close()


