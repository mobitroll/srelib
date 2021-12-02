#!/usr/bin/env python3
# encoding: utf-8

import sys

from srelib.aws import Aws


if __name__ == "__main__":
    aws = Aws()

    try:
        region = sys.argv[1]
    except IndexError:
        print(f"Usage {sys.argv[0]} <region>")
        sys.exit(1)

    instances = aws.get_ec2_instances(region)
    for i in instances:
        print(i)
