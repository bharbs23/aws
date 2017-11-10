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
filepath = r'C:\Users\bharbs\Desktop\aws_scripts\scripts\output\output_3.csv'
csv_file = open(filepath,'w')	


csv_file.write("*******creating snapshot which are tagged to production****\n")		
def main():
	#List all volumes
	volumes = conn.get_all_volumes()
	#Getting EBS Volumes which are tagged to production
	for volume in volumes:
		if 'Name' in volume.tags:
			TagName = volume.tags['Name']
			TagName = TagName.lower()
			print TagName
			csv_file.write("%s\n"%(TagName))
			#csv_file.write("%s\n"%(' '))
			
			if TagName.find('production') != -1:
					
				volume_id = volume.id
				print volume_id
				csv_file.write("%s\n"%(volume.id))
				#csv_file.write("%s\n"%(' '))
					
				snapshot = conn.create_snapshot(volume_id, "EC2 daily snapshot")
				print snapshot.id
				csv_file.write("%s\n"%(snapshot.id))
				#csv_file.write("%s\n"%(' '))

				#creating snapshot which are tagged to production
				snaps = conn.get_all_snapshots(filters={'volume-id':volume_id})
				for i in snaps:
					print i,i.start_time
					csv_file.write("%s\t%s\n"%(i,i.start_time))
					date = i.start_time
					date1 = date[:-14]
					print "date1", date1
					csv_file.write("%s\t%s\n"%("date1",date1))
					y = date1[:-6]
					y = int(y)
					m = date[5:-17]
					m = int(m)
					d = date1[8:]
					d = int(d)
					d1 = datetime.date(y,m,d)
					print "snapshot creation date", d1
					csv_file.write("%s\t %s\n"%("snapshot creation date",d1))
					today = datetime.date.today()

					diff = today - d1
					diff1 = diff.days
					print diff1
					csv_file.write("%d\n"%(diff1))

					if diff1 <= 7:
						print "do not delete snapshot"
						csv_file.write("do not delete snapshot\n")
					else:
						print "delete snapshot"
			elif TagName != 'Production':
				print 'this volumes not attached as production'
				csv_file.write('this volumes not attached as production\n')
		else:
			print "%s  (%s)" % (volume.id,volume.attach_data.instance_id)
    

		
if __name__ == '__main__':
    main()