import boto.cloudtrail
import argparse
from boto import *
from botocore import xform_name
import botocore.session
from botocore.client import ClientError
from botocore.vendored.requests import adapters
from botocore.vendored.requests.exceptions import ConnectionError
import boto3
import json

##parser = argparse.ArgumentParser(prog='Attributes Collection')
##parser.add_argument('--region')
##args = parser.parse_args()


##def get_cloudtrail_regions():
##    """ Return list of names of regions where CloudTrail is available """
##
##    cloudtrail_regioninfo_list = boto.regioninfo.get_regions('cloudtrail')
##    return [r.name for r in cloudtrail_regioninfo_list]
##
##def get_cloudtrail_trail(region):
##    ct_conn = boto.cloudtrail.connect_to_region(region_name='us-east-1')
##    trail_list = ct_conn.describe_trails()
##    for line in trail_list['trailList']:
##        if line == 'None':
##            return ("Failed")
##        else:
##            return trail_list['trailList'][0]['Name']
##
##print(get_cloudtrail_trail('us-west-2'))


ct_conn = boto3.client(service_name='cloudtrail',region_name='us-east-2')
#print ct_conn
inst_tstst=[]
events_dict= ct_conn.lookup_events(LookupAttributes=[{'AttributeKey':'ResourceName', 'AttributeValue':'i-075931a3fac6938fa'}])
#print events_dict
for data in events_dict['Events']:
         
        json_file= json.loads(data['CloudTrailEvent'])
        inst_tstst.append(json_file['userIdentity']['userName']+' - '+json_file['eventName']+' - '+json_file['eventTime']+' - '+json_file['eventType'])
print inst_tstst[0]

