#!/usr/bin/env python2
import boto.ec2
import datetime
import configparser


config = configparser.RawConfigParser()
configFilePath = r'C:\Users\bharbs\Desktop\python\test.txt'
config.read(configFilePath)

try:
	REGION = config.get('file', 'REGION')
	aws_access_key_id = config.get('file', 'aws_access_key_id')
	aws_secret_access_key = config.get('file', 'aws_secret_access_key')

except ConfigParser.NoOptionError :
    print('could not read configuration file')
    sys.exit(1)  
	
	
conn = boto.ec2.connect_to_region(REGION,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
print conn	
filepath = r'C:\Users\bharbs\Desktop\aws_scripts\scripts\output\output_2.csv'
csv_file = open(filepath,'w')	


#List all volumes
csv_file.write("*********List all volumes*************\n")		
def main():
	volumes = conn.get_all_volumes()
	for volume in volumes:
		if 'Name' in volume.tags:
			print "%s (%s) (%s)" % (volume.tags['Name'], volume.id,volume.attach_data.instance_id)
		else:
			print "%s  (%s)" % (volume.id,volume.attach_data.instance_id)
		csv_file.write("%s\t %s\t %s\n"%(volume.tags['Name'],volume.id,volume.attach_data.instance_id))

		
if __name__ == '__main__':
    main()