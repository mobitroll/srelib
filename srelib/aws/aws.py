# encoding: utf-8

import logging

import boto3

from .config import Config


class Aws:
    def __init__(self):
        self.config = Config()

    def get_events_list(self):
        # FIXME remove hardcoded regions list
        regions = ['us-east-1', 'us-west-1', 'eu-west-1', 'ap-southeast-2']
        event_list = []

        for region in regions:
            logging.info(f"Loading events for region {region}")

            client = boto3.client('ec2', aws_access_key_id=self.config.aws_access_key_id,
                                  aws_secret_access_key=self.config.aws_secret_access_key,
                                  region_name=region)
            response = client.describe_instance_status(IncludeAllInstances=True)

            for status in response['InstanceStatuses']:
                if 'Events' in status:
                    for event in status['Events']:
                        event_list.append((
                            region,
                            status['InstanceId'],
                            status['AvailabilityZone'],
                            event['Code'],
                            event['NotBefore'],  # NotBeforeDeadline
                        ))

        return event_list

    def get_ec2_instances(self, aws_region, server_group=None):
        # validate_domain(domain)

        if aws_region != 'all':
            # validate_aws_region(aws_region)
            pass

        def get_servers(region, server_group=None):
            server_results = []
            client = boto3.client('ec2', region_name=region,
                aws_access_key_id=self.config.aws_access_key_id,
                aws_secret_access_key=self.config.aws_secret_access_key)

            paginator = client.get_paginator('describe_instances')

            def get_instance_name(instance):
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        return tag['Value']

            for response in paginator.paginate():

                for record in response['Reservations']:
                    instance = record['Instances'][0]
                    if instance['State']['Name'] != 'running':
                        continue

                    securitygroup = instance['SecurityGroups'][0]['GroupName']

                    if server_group is None or (server_group and securitygroup == server_group):
                        server_results.append({
                            'name': get_instance_name(instance),
                            'instanceid': instance['InstanceId'],
                            'ip': instance['PublicIpAddress'],
                            'dns': instance['PublicDnsName'],
                            'region': region,
                            'launchtime': instance['LaunchTime']})

            return server_results

        return get_servers(aws_region, server_group)
