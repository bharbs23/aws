import boto.ec2
import datetime
conn=boto.ec2.connect_to_region("us-east-2",aws_access_key_id="AKIAJLDSCKBDJPGYE44A",aws_secret_access_key="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")
volumes = conn.get_all_volumes()
for volume in volumes:
	if 'Name' in volume.tags:
		TagName = volume.tags['Name']
		TagName = TagName.lower()
		print TagName
		if TagName.find('production') != -1:
			
			volume_id = volume.id
			print volume_id
			
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
			print 'No volumes attached to production'
	else:
		print "%s  (%s)" % (volume.id,volume.attach_data.instance_id)