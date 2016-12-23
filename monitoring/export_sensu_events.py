import argparse
from sensu import Pysensu
import json
import csv
from pprint import pprint as pp

# Fields we want to capture for Sensu Json API output
fields = [
        'last_ok',
        'silenced',
]
check_fields = [
        'name',
        'command',
        'team',
        'output',
        'region',
]

def iter_events(sensu_client, ignore_status=0):
    ''' iterate through sensu events and returns dict of fields '''
    events = sensu_client.get_all_events()
    for event in events:
        if event['check']['status'] == ignore_status:
            continue
        field_dict = {f : event.get(f, None) for f in fields}
        check_dict = {f : event['check'].get(f, None) for f in check_fields}
        # Concatenate both dicts into one
        line = {**field_dict, **check_dict} # only works in python 3.5, nice !
        yield line

def main():
    parser = argparse.ArgumentParser("Connect to Sensu export as CSV")
    parser.add_argument('-H', action="store", dest="host", help="Sensu Host")
    parser.add_argument('-u', action="store", dest="username", help="Username")
    parser.add_argument('-p', action="store", dest="password", help="Password")
    parser.add_argument('-o', action="store", dest="outfile", help="output file")
    args = parser.parse_args()

    client = Pysensu(args.host, args.username, args.password)
    allfields = fields + check_fields
    headers = { n: n for n in allfields }
    fieldnames = tuple(headers)
    with open(args.outfile, 'wt') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for event in iter_events(client):
            writer.writerow(event)


if __name__ == '__main__':
    main()
