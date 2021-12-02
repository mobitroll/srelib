#!/usr/bin/env python3
# encoding: utf-8

import sys

from srelib.datadog import Datadog


if __name__ == "__main__":
    datadog = Datadog()

    try:
        hosts_filter = sys.argv[1]
    except IndexError:
        print("Usage: datadog_hosts.py <hosts_filter>")

    hosts = datadog.get_hosts(hosts_filter)

    for host in hosts.get('host_list', []):
        name = host['host_name']
        tags = host['tags_by_source']['Datadog'] or []
        aws_id = host['aws_id'] or None

        ip = None
        for tag in tags:
            if "public_ip:" in tag:
                ip = tag[10:]
                break

        # import json
        # print(json.dumps(host, sort_keys=True, indent=4))

        link = f"https://app.datadoghq.com/infrastructure?host={name}"
        print(f"{name}\t{ip}\t{aws_id}\t{link}")
