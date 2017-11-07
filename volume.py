#!/usr/bin/env python2
import boto.ec2
import datetime

REGION = 'us-east-2'
conn = boto.ec2.connect_to_region(REGION,aws_access_key_id="AKIAJLDSCKBDJPGYE44A",aws_secret_access_key="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")

def main():
	#List all instances
	reservations = conn.get_all_instances()
	for res in reservations:
		for inst in res.instances:
			if 'Name' in inst.tags:
				print "%s (%s) [%s]" % (inst.tags['Name'], inst.id, inst.state)
			else:
				print "%s [%s]" % (inst.id, inst.state)
				
				
    #List all volumes
	volumes = conn.get_all_volumes()
	for volume in volumes:
		if 'Name' in volume.tags:
			print "%s (%s) (%s)" % (volume.tags['Name'], volume.id,volume.attach_data.instance_id)
		else:
			print "%s  (%s)" % (volume.id,volume.attach_data.instance_id)
	
	#Getting EBS Volumes which are tagged to production
	for volume in volumes:
		if 'Name' in volume.tags:
			TagName = volume.tags['Name']
			TagName = TagName.lower()
			print TagName
			if TagName.find('production') != -1:
				
				volume_id = volume.id
				print volume_id
				
				
				#creating Snapshots for EBS Volumes which are tagged to production 
				snapshot = conn.create_snapshot(volume_id, "EC2 daily snapshot")
				print snapshot.id


				snaps = conn.get_all_snapshots(filters={'volume-id':volume_id})
				for i in snaps:
					print i,i.start_time
					date = i.start_time
					date1 = date[:-14]
					print "date1", date1
					y = date1[:-6]
					y = int(y)
					m = date[5:-17]
					m = int(m)
					d = date1[8:]
					d = int(d)
					d1 = datetime.date(y,m,d)
					print "snapshot creation date", d1

					today = datetime.date.today()

					diff = today - d1
					diff1 = diff.days
					print diff1

					if diff1 <= 7:
						print "do not delete snapshot"
					else:
						print "delete snapshot"
			elif TagName != 'Production':
				print 'this is not attached as Production'
		else:
			print "%s  (%s)" % (volume.id,volume.attach_data.instance_id)
        # # Object attributes:
        # print volume.__dict__

        # # Object methods:
        # print(dir(volume))

if __name__ == '__main__':
    main()