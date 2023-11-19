import sys
import re
from collections import defaultdict

def process_file(file_name):
    data = []
    with open(file_name, 'r') as file:
        for line in file:
            if 'emThriftAPI' in line:
                parts = line.split()
                try:
                    date = re.sub(r'^\[.*20..:', '', parts[4])
                    svc = re.sub(r'/emThriftAPI/', '', parts[12])
                    bytes = int(parts[11])
                    milliseconds = int(parts[13])
                    data.append((date, svc, bytes, milliseconds))
                except (IndexError, ValueError):
                    continue  # Skip lines that don't have the expected format
    return data

def main(log_files):
    all_data = []
    for log_file in log_files:
        all_data.extend(process_file(log_file))

    services = sorted(set([svc for _, svc, _, _ in all_data]))
    stats = defaultdict(lambda: {'total_reqs': 0, 'total_bytes': 0, 'total_milliseconds': 0, 'begin_date': '', 'end_date': ''})

    for date, svc, bytes, milliseconds in all_data:
        if stats[svc]['total_reqs'] == 0:
            stats[svc]['begin_date'] = date
        stats[svc]['end_date'] = date
        stats[svc]['total_reqs'] += 1
        stats[svc]['total_bytes'] += bytes
        stats[svc]['total_milliseconds'] += milliseconds

    for svc in services:
        print('^^^^^^^^^^^^^^^^^^^^^')
        print(f'SVC: {svc}')
        stat = stats[svc]
        print(f"\ntime frame: {stat['begin_date']} {stat['end_date']}")
        print(f"total reqs: {stat['total_reqs']}  bytes: {stat['total_bytes']} milliseconds: {stat['total_milliseconds']}")

if __name__ == "__main__":
    main(sys.argv[1:])
