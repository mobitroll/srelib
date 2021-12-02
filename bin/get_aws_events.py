#!/usr/bin/env python3
# encoding: utf-8

from srelib.aws import Aws


if __name__ == "__main__":
    aws = Aws()

    def event_date(event_record):
        return event_record[3]

    for event in sorted(aws.get_events_list(), key=event_date):
        region = event[0]
        instance_id = event[1]
        az = event[2]
        event_type = event[3]
        date = event[4]

        print(f"{region}\t{instance_id}\t{event_type}\t{date}")