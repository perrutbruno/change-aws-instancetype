import boto3

client = boto3.client('ec2')


instance_list = []

# Open the file with read only permit
f = open('lista.txt', "r")
# use readlines to read all lines in the file
# The variable "lines" is a list containing all lines in the file
lines = f.readlines()
# close the file after reading the lines.
f.close()
for line in lines:
    instance_list.append(line[:-1])

def change_instancetype(instanceid):
    # Change the instance type
    client.modify_instance_attribute(InstanceId=instanceid, Attribute='instanceType', Value='m5.xlarge')
    f = open("logs.txt", "a")
    f.write(f"instancia {instanceid} trocado instancetype para m5.xlarge!")
    f.close()


def get_status_code(instanceid):
    describe_instances = client.describe_instances(
            Filters=[
                {
                    'Name': 'instance-id',
                    'Values': [
                        instanceid,
                    ],
                },
            ],
        )


    for row in describe_instances['Reservations']:
        for instances in row['Instances']:
            status_final = instances['State']['Name']
            return status_final


for index in instance_list:
    status = get_status_code(index)
    if status == 'stopped':
        try:
            change_instancetype(index)
        except Exception as e:
            pass
    else:
        print(f'Instance {index} is not in stopped state')
        f = open("logs.txt", "a")
        f.write(f"instancia {index} desligada!")
        f.close()