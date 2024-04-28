import boto3
from tabulate import tabulate

session = boto3.Session(profile_name='aws-cloud', region_name='us-east-1')
sts_client = session.client('sts')
response = sts_client.assume_role(
    RoleArn='arn:aws:iam::502433561161:role/aws-cloud',
    RoleSessionName='python-boto3')

aws_access_key_id = response['Credentials']['AccessKeyId']
aws_secret_access_key = response['Credentials']['SecretAccessKey']
aws_session_token = response['Credentials']['SessionToken']
new_session = boto3.Session(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            aws_session_token=aws_session_token,
                            region_name='us-east-1')
client_obj = new_session.client('ec2')
AWS_ACCOUNTS = ['502433561161']
serial_no = []
vpc_record = []

for each_account in AWS_ACCOUNTS:
    VPC_ids = []
    VPC_cidrs = []
    for each_region in client_obj.describe_regions()['Regions']:
        filter = [{'Name': 'tag:Name', 'Values': ['*']}]
        vpc_response = client_obj.describe_vpcs(Filters=filter)['Vpcs']
        for each_vpc in vpc_response:
            VPC_ids.append(each_vpc['VpcId'])
            VPC_cidrs.append(each_vpc['CidrBlock'])

    # print(VPC_ids)
    # print(VPC_cidrs)
    
    v = 0
    for vpc_id in VPC_ids:
        subnet_response = client_obj.describe_subnets(
            Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
        vpc_cidr = VPC_cidrs[v]
        for each_subnet in subnet_response['Subnets']:
            aws_account = []
            list_of_all_Regions = []
            list_of_all_VPC_ids = []
            list_of_all_VPC_cidrs = []
            list_of_all_subnet_ids = []
            list_of_all_subnet_cidrs = []
            list_of_all_subnet_AZs = []
            count_of_available_ips = []
            aws_account.append(each_account)
            list_of_all_Regions.append(each_region['RegionName'])
            # list_of_all_VPC_ids.append(each_vpc_id['VpcId'])
            # list_of_all_VPC_cidrs.append(each_vpc['CidrBlock'])
            list_of_all_VPC_ids.append(vpc_id)
            list_of_all_VPC_cidrs.append(vpc_cidr)
            list_of_all_subnet_ids.append(each_subnet['SubnetId'])
            list_of_all_subnet_cidrs.append(each_subnet['CidrBlock'])
            count_of_available_ips.append(
                each_subnet['AvailableIpAddressCount'])
            list_of_all_subnet_AZs.append(each_subnet['AvailabilityZone'])
            vpc_record.append(aws_account + list_of_all_Regions + list_of_all_VPC_ids + list_of_all_VPC_cidrs +
                              list_of_all_subnet_ids + list_of_all_subnet_cidrs + count_of_available_ips + list_of_all_subnet_AZs)
        v = v+1
        
# print(list_of_all_VPC_ids)
# print(list_of_all_VPC_cidrs)
# print(list_of_all_Regions)
# print(vpc_record)

headers = ["AWS Account #"]+["AWS Region"]+["VPC-ID"] + \
    ["VPC-CIDR"]+["SUBNET-ID"]+["SUBNET-CIDR"] + \
    ["AVAILABLE IPs"]+["Availability Zone"]
print(tabulate(vpc_record, headers=headers, tablefmt="heavy_grid"))
