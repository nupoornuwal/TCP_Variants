import subprocess
import os  
import sys
from operator import sub
import openpyxl
from openpyxl import Workbook
ns_command= "/course/cs4700f12/ns-allinone-2.35/bin/"
import pylab

variant= ["Reno","SACK"]
queue_variant=["DropTail","RED"]

for var in variant:
	for k in queue_variant :
		os.system("cd " +ns_command)
                os.system('ns '+'testqueue.tcl '+var+' '+k)	


def plt(a,b,c,d,e,f,g,h):
		for i in range(len(d)):
			d[i]=d[i]*0.1		
		pylab.figure(1)
        	pylab.plot(a,b)
                pylab.plot(c,d)
		pylab.plot(e,f)
                pylab.plot(g,h)
		#pylab.plot(i,j)
                pylab.grid()
		pylab.title('Latency')
                pylab.xlabel('Time(s)')
                pylab.ylabel('Latency(s)')
                pylab.legend(['Reno_Droptail','Reno_RED','SACK_Droptail','SACK_RED'])
                pylab.show()


def throughput(var,k):
        global thoughtput
        file='testqueue'+var+k+'.tr'
        #print 'FILE', file
        f=open(file)
        lines=f.readlines()
        #print lines
        f.close()
	start_received_time1=0.0
	start_received_time2=0.0
        received_packet1=0
        received_packet2=0
        start_time=0.0
        start_time1=0.0
        end_time1=0.0
        end_time2=0.0
        through_list=[]
        through_list1=[]
        x=0.25
        y=10.0
	time_list=[]
	time_list1=[]
        for k in lines:
                #print k
                n=k.split()
                if n[7]=="1":
			if n[0]=="+" and n[2]=="0" and n[4]=="tcp":
					if start_time==0.0:
						start_time=float(n[1])
		                                #print start_time		
                        if n[0]== "r" and  n[3]== "4" and n[4]=="tcp" :
                                        received_packet1=received_packet1+int(n[5])
                                        end_time1=float(n[1])
					#difference=end_time1-start_time
                                        #print 'end_time1',end_time1
                        if  float(n[1])>=x:
				
				difference=end_time1-start_time
				#print 'Difference',difference
				time_list.append(float(n[1]))
                                through=(received_packet1*8)/(difference*1000000)
                                through_list.append(through)
                                x+=0.25
				start_time=0.0
				received_packet1=0

                if n[7]=="2":
				
			if n[0]=="+" and n[2]=="1" and n[4]=="cbr":
                                        if start_time1==0.0:
                                                start_time1=float(n[1])
						print start_time1
                        if n[0]== "r" and  n[3]== "5" and n[4]=="cbr" :
                                        received_packet2=received_packet2+int(n[5])
                                        end_time2=float(n[1])
                                        print 'end_time2',end_time2
                        if float(n[1])>=y:
				difference1=end_time2-start_time1
				print 'DIFFERENCE',difference1
				time_list1.append(float(n[1]))
                                through1=received_packet2*8/(difference1*1000000)
                                through_list1.append(through1)
                                y+=0.25
				start_time1=0.0
				received_packet2=0
				


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
        #print 'throughlist',through_list, len(through_list)
	#print 'time1',time_list,len(time_list)
        #print 'throughlist1',through_list1
        return time_list,through_list,time_list1,through_list1


def latency(var,k):
        file='testqueue'+var+k+'.tr'
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
	lat_average=[]
	lat_average1=[]
	lat_time=[]
	lat_time1=[]
	u=1.0
	v=11.0
	for k in lines:
             #print k
             n=k.split()
             if n[7]=='1':
                if n[0]=="+" and n[2]=="0" and n[3]=='2' and  n[4]=="tcp":
			if n[10] not in seq_num:     #check for retransmission
				seq_num.append(n[10]) 
                                start_tup=(n[10],n[1])
                                c.append(start_tup)
				#print 'START TUP',start_tup
                if n[0]=="r" and n[3]=="4" and n[4]=="tcp":
                                b=n[10]
                                for tup in c:
					#print "tuple",tup
                                        if n[10] in tup:
                                                        start_time=float(tup[1])
                                                        latency= float(n[1])-start_time
                                                        latency_list.append(latency)
							#print 'CHECK',latency_list
							#print 'len', len(latency_list)
		if float(n[1])>=u:
			#print 'ALLLLLLLLIIIIIIIIIIIIIIIIIIIVVVVVVEEEEEEEEEEEEEEEEEEEE'
			#print 'LATENCY',latency_list,len(latency_list)
			avg_lat=float(sum(latency_list)/len(latency_list))
			lat_average.append(avg_lat)
			lat_time.append(float(n[1]))
			u+=0.25
			latency_list=[]
	     if n[7]=='2':
                if n[0]=="+" and n[2]=="1" and n[3]=='2' and n[4]=='cbr':
                        if n[10] not in seq_num1:
                                seq_num1.append(n[10])
                                start_tup1=(n[10],n[1])
                                c1.append(start_tup1)
				#print  'second list' ,c1
                if n[0]=="r" and n[3]=="5" and n[2]=='3' and n[4]=='cbr':
                                b=n[10]
                                for tup in c1:
                                        #print "tuple",tup
                                        if n[10] in tup:
                                                        start_time1=float(tup[1])
                                                        latency1= float(n[1])-start_time1
                                                        latency_list1.append(latency1)
							#print 'latency_list1',len(latency_list1)
							         
       		if float(n[1])>=v:
			#print 'DDDDDDDDDDDDDDDDDDDDDDDDDDEEEEEEEEEEEEEEEEEEEEEEEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
			#print 'latency_list1',len(latency_list1)
			avg_lat1=float(sum(latency_list1)/len(latency_list1))
                        lat_average1.append(avg_lat1)
			lat_time1.append(float(n[1]))
                        v+=0.25
			latency_list1=[]
	#print 'latency_list1',len(latency_list1)
	#print 'latency_list',len(latency_list)
        #average_latency=sum(latency_list)/len(latency_list)
	#average_latency1=sum(latency_list1)/len(latency_list1)
        #print 'AverageLatency:', average_latency 
	#return str(average_latency1) + '\t' + str(average_latency1)
	return lat_time,lat_average,lat_time1,lat_average1,
for var in variant:
	for val in queue_variant:
		if var=="Reno" and val=="DropTail": 
			a=[]
			b=[]
			c=[]
			d=[]
			a,b,c,d=latency(var,val)
			
		if var=="Reno" and val=="RED":
                        e=[]
                        f=[]
			g=[]
                        h=[]
                        e,f,g,h=latency(var,val)
			#p(a,b,c,d,2,'Reno/RED')
		if var=="SACK" and val=="DropTail":
                        i=[]
                        j=[]
                        k=[]
                        l=[]
                        i,j,k,l=latency(var,val)
			#p(a,b,c,d,3,'SACK/Droptail')
                        
		if var=="SACK" and val=="RED":
                        m=[]
                        n=[]
                        o=[]
                        p=[]
                        m,n,o,p=latency(var,val)
			plt(a,b,e,f,i,j,m,n)
      



