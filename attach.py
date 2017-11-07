from boto.ec2.connection import EC2Connection

conn = EC2Connection(aws_access_key_id="AKIAJGS7V3NG2YXVNFCQ",aws_secret_access_key="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")
res = conn.get_all_instances()
instances = [i for r in res for i in r.instances]
vol = conn.get_all_volumes()
def attachedvolumes():
    print 'Attached Volume ID - Instance ID','-','Device Name'
    for volumes in vol:
        if volumes.attachment_state() == 'attached':
            filter = {'block-device-mapping.volume-id':volumes.id}
            volumesinstance = conn.get_all_instances(filters=filter)
            ids = [z for k in volumesinstance for z in k.instances]
            for s in ids:
                 print volumes.id,'-',s.id,'-',volumes.attach_data.device
# Get a list of unattached volumes           
"""def unattachedvolumes():
   for unattachedvol in vol:
       state = unattachedvol.attachment_state()
   if state == None:
        print unattachedvol.id, state
#unattachedvolumes()"""
attachedvolumes()