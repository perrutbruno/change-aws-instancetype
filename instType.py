import boto3, time

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
    client.modify_instance_attribute(InstanceId=instanceid, Attribute='instanceType', Value='t2.medium')
    f = open("logs.txt", "a")
    f.write(f"instancia {instanceid} trocado instancetype para t2.medium!")
    f.close()

def shutdown_instance(instanceid):
    client.stop_instances(InstanceIds=instanceid, DryRun=True)

def start_instance(instanceid):
    client.start_instances(InstanceIds=instanceid, DryRun=True)

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
            start_instance(index)
        except Exception as e:
            pass
    elif status == 'running':
        shutdown_instance(index)
        time.sleep(120)
        try:
            change_instancetype(index)
            start_instance(index)

        except Exception as e:
            f = open("logs.txt", "a")
            f.write("************************************!")
            f.write(f"instancia {index} nao esta desligada, favor rodar novamente mais tarde. Except {e}")
            f.write("************************************!")
            f.close()

    else:
        print(f'Instance {index} is not in stopped / started state!')
        f = open("logs.txt", "a")
        f.write(f"Instance {index} is not in stopped / started state!")
        f.close()