import boto3
from collections import defaultdict
import time

class server:

    def __init__(self, imageId, instanceType, keyPairName):
        aws = boto3.Session(aws_access_key_id='YOURACCESSKEY', aws_secret_access_key='YOURSECRETACCESSKEY', region_name='eu-central-1')
        self.IDS = []
        self.keyPairName = keyPairName
        self.ec2 = aws.resource('ec2')
        self.imageId = imageId
        self.instanceType= instanceType
        self.IP = []
        self.instances = self.ec2.instances.filter(Filters=[{
                                                                                          'Name': 'instance-state-name',
                                                                                          'Values': ['pending', 'running']}])
        self.runningInstances = self.ec2.instances.filter(Filters=[{
                                                                                          'Name': 'instance-state-name',
                                                                                          'Values': ['running']}], InstanceIds=self.IDS)
       
        
    def  createKeyPair(self):
        outfile = open('pubkey.pem','w')
        keyPair = self.ec2.create_key_pair(KeyName=self.keyPairName)
        keyPairOut = str(keyPair.key_material)
        print(keyPairOut)
        outfile.write(keyPairOut)
        

    def createServer(self, count):
        instances = self.ec2.create_instances(
                                                                ImageId=self.imageId,
                                                                MinCount=1,
                                                                MaxCount=count,
                                                                InstanceType=self.instanceType,
                                                                KeyName=self.keyPairName)


    def getInstancesList(self):
        self.IP.clear()
        for instance in self.instances:
            self.IP.append(instance.public_ip_address)

           
    def attachSecurityGroups(self):
        for instance in self.instances:
            instance.modify_attribute(Groups = ['sg-067b6242587dd5fdd'])


    def deleteServers(self, deleteCount):
        for instance in self.runningInstances:
            self.IDS.append(instance.id)
        self.ec2.instances.filter(InstanceIds=self.IDS[0:deleteCount],
                                                 Filters=[{'Name': 'instance-state-name',
                                                                'Values': ['running']}]).terminate()

##  if __name__ == '__main__':
def program():

    while True:
        command = input('Enter command: ')

        if command == 'Update keypair':
            key = str(input('Enter keyname: '))
            session = server('ami-0c5fc0aef1db27ff7', 't2.micro', key)
            session.createKeyPair()

        if command == 'Create proxy':
            count = int(input('Enter count: '))
            session.createServer(count)
            time.sleep(10)
            session.getInstancesList()
            for i in range (len(session.IP)):
                print(session.IP[i]+':8888')
            session.attachSecurityGroups()

        if command == 'Delete proxy':
            deleteCount = int(input('Enter count: ')) 
            session.deleteServers(deleteCount)
            time.sleep(10)
            session.getInstancesList()
            print('Current proxy: ')
            for i in range (len(session.IP)):
                print(session.IP[i]+':8888')

program()
        

            

        

        
                                            


