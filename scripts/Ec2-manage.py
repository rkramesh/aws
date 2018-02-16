from __future__ import print_function
from pprint import pprint
from boto import ec2,boto,re
import boto3,json,yaml,time
d = lambda x,y=15: 'None'.ljust(y) if x is None else x.ljust(y)
Ntag=(lambda x: 'Name not Assigned' if x is None else x[0]['Value'])
class Ec2Connect(object):
    @staticmethod
    def menu():
        print ("Enter '1' to list All Available Ec2 instances: ")
        print ("Enter '2' to list  Stopped Ec2 instances: ")
        print ("Enter '3' to list Currently  Running Ec2 instances: ")
        print ("Enter '4' to list Instances with Cloudtrial data: ")
        print ("Enter '5' to start/stop Ec2 instances: ")
        choice = int(raw_input("\n>Enter Your Option here: "))
        if choice == 1:
            Ec2Connect.main(dis='Manage')
            instflist=sorted(instlist, key=lambda sortid: sortid[0])
            [ print(x) for x in instflist ]
        elif choice == 2:
             Ec2Connect.main()
             [ print(x) for x in instlist if x.startswith('st')]
        elif choice == 3:
            Ec2Connect.main()
            [ print(x) for x in instlist if x.startswith('run')]
        elif choice == 4:
            print ("Warning !!!Fetching details from CloudTrial will take more than 50 seconds!!!")
            Ec2Connect.main(dis=False)
            instflist=sorted(instlist, key=lambda sortid: sortid[0])
            [ print(x) for x in instflist ]
        elif choice == 5:
            Ec2Connect.ec2Manage()
        else:
            print ('Enter the correct choice!')
    @staticmethod
    def ec2Manage():
        ins_tag={}
        ins_stat={}
        ins_reg={}
        insid={}
        Ec2Connect.main(dis='Manage')
        instf=sorted(instid, key=lambda sortid: sortid[0])
        print ("\n" * 100)
        for count,tag in enumerate (instf):
            count+=1
            print ("Enter {0} to Start/Stop {1}({3})- {4}{2}  ".format(d(str(count),2),d(tag[5],30),d(tag[0]),d(tag[3],15),d(tag[4])))
            insid[count]=tag[3]
            ins_tag[count]=tag[5]
            ins_stat[count]=tag[0]
            ins_reg[count]=tag[1]
        choice = int(raw_input("\n>Enter Your Option here: "))
        while not 1 <= choice <= count: 
             print('Wrong Choice!,Enter the correct choice.\n')
             choice = int(raw_input("\n>Enter Your Option here: "))
##        conn = boto.ec2.connect_to_region(ins_reg[choice][:-1])
        conn = boto3.client('ec2',region_name=ins_reg[choice][:-1])
        if ins_stat[choice] == 'stopped':
            print ("Are you sure you want to Start these instances ? \n  =>{} ({}) \n".format(ins_tag[choice],insid[choice]))
            raw_input("Press Any Key to Continue  or CTRL+C to exit!...")
            print ("Starting Instance {} ({}) ".format(ins_tag[choice],insid[choice]))
            conn.start_instances(InstanceIds=[insid[choice]])
        elif ins_stat[choice] == 'running':
            print ("Are you sure you want to stop these instances ? \n  =>{} ({}) \n \
Please note that Any data on the ephemeral storage of your instances will be lost.\n".format(ins_tag[choice],insid[choice]))
            raw_input("Press Any Key to Continue  or CTRL+C to exit!...")
            print ("stopping Instance {} ({}) ".format(ins_tag[choice],insid[choice]))
            conn.stop_instances(InstanceIds=[insid[choice]])
        else:
            print('Wrong Choice!,Enter the correct choice.')
    @staticmethod    
    def listAll_Ec2time(region,dis,iiid):
        ct_conn = boto3.client(service_name='cloudtrail',region_name=region)
        inst_tstst=[]
        events_dict= ct_conn.lookup_events(
        LookupAttributes=[
                {
                    'AttributeKey': 'ResourceName',
                    'AttributeValue': iiid
                }
            ],
           MaxResults=1
        )
        for data in events_dict['Events']:
            if data['CloudTrailEvent']:
                json_file= json.loads(data['CloudTrailEvent'])
##                return (json_file['userIdentity']['arn']).split('/')[1]
                return ((json_file['userIdentity']['arn']).split('/')[-1]+' - '+json_file['eventName']+' - '+json_file['eventTime'])
            else:
                return ('7 day data not found')
        return 'CloudTrail data Not available!'
    @staticmethod
    def listAll_Ec2(region,dis):
        ec2 = boto3.resource('ec2', region_name=region)
        instances = ec2.instances.filter()
##        instances=[ instance["InstanceId"] for reservation in response["Reservations"]for instance in reservation["Instances"]]
        for i in instances:
##            pprint(i.__dict__)
            if dis==True:
                instlist.append( d(i.state['Name'],10)+d(i.placement['AvailabilityZone'])+ d(i.public_ip_address)+ d(i.platform,10)+d(i.private_ip_address,16)+d(i.instance_type,10)\
                             +d(Ntag(i.tags),30))
            elif dis==False:
                instlist.append( d(i.state['Name'],10)+d(i.placement['AvailabilityZone'])+ d(i.public_ip_address)+ d(i.platform,10)+d(i.private_ip_address,16)+d(i.instance_type,10)\
                             +d(Ntag(i.tags),30)+d(Ec2Connect.listAll_Ec2time(region,dis=True,iiid=i.id)))
            elif dis=='Manage':
                instid.append([i.state['Name'],i.placement['AvailabilityZone'],i.platform,i.id,i.instance_type,Ntag(i.tags)])
                
            else:
                instlist.append( d(i.state['Name'],10)+d(i.placement['AvailabilityZone'])+ d(i.public_ip_address)+ d(i.platform,10)+d(i.private_ip_address,16)+d(i.instance_type,10)\
                             +d(Ntag(i.tags),30))
##                instid.append([i.state['Name'],i.placement['AvailabilityZone'],i.platform,i.id,i.instance_type,Ntag(i.tags)])

            global run,stop
            if i.state['Name'] == 'running':
                run +=1
            elif i.state['Name'] == 'stopped':
                stop +=1
    @staticmethod            
    def main(dis=False):
        regions = ['us-east-1','us-west-1','us-west-2','us-east-2','eu-central-1']
        print ('Fetching Instances from All available regions...')
        print (d('State',10)+d('Region')+ d('Public_dns')+d('Platform',10)+d('Private Ip',16)\
               +d(' Type')+d('Name'))
        print (d('='*142,1))
        for region in regions:  Ec2Connect.listAll_Ec2(region,dis)
while True:
    print ("\n" * 100)
    run=stop=0
    instlist=[]
    instid=[]
    start_time = time.time()
    Ec2Connect.menu()
    print("{} Executed in {} seconds {} ".format ("="*54,time.time() - start_time,"="*54))
    print ('All  available Ec2 Instances: '+ str( run+stop))
    print ('Currently Running Ec2 Instances: '+ str(run))
    print ('Stopped Ec2 Instances: '+ str(stop))
    raw_input("Press Any Key to Continue  or CTRL+C to exit!...")
