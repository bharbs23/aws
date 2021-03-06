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
filepath = r'C:\Users\bharbs\Desktop\aws_scripts\scripts\output\output_1.csv'
csv_file = open(filepath,'w')


#list all instances
csv_file.write("***********list all instances***************\n")		
def main():
	reservations = conn.get_all_instances()
	for res in reservations:
		for inst in res.instances:
			if 'Name' in inst.tags:
				print "%s (%s) [%s]" % (inst.tags['Name'], inst.id, inst.state)
			else:
				print "%s [%s]" % (inst.id, inst.state)
		csv_file.write("%s\t %s\t %s\n"%(inst.tags['Name'], inst.id, inst.state))		

		
if __name__ == '__main__':
    main()