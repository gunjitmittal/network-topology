import pandas as pd
from itertools import groupby
from pprint import pprint

# Step 1: Read ip.csv to create a mapping of IP addresses to AS numbers
ip_as_mapping = pd.read_csv('ip.csv')
ip_as_mapping = ip_as_mapping.iloc[:, :2]
ip_as_mapping = dict(ip_as_mapping.values)

# Step 2: Read out.csv and replace IP-based edges with AS-based edges
as_edges = []
out_df = pd.read_csv('out.csv')
for _, row in out_df.iterrows():
    src_ip, dst_ip, domain, label, ttl = row
    src_as = ip_as_mapping.get(src_ip)
    dst_as = ip_as_mapping.get(dst_ip)
    as_edges.append([src_as, dst_as, domain])

paths = {}
for edge in as_edges:
    if edge[2] not in paths: paths[edge[2]] = []
    if edge[0] is not None: paths[edge[2]].append(edge[0])
    if edge[1] is not None: paths[edge[2]].append(edge[1])

for domain in paths:
    paths[domain] = [i[0] for i in groupby(paths[domain])]

pprint(paths)

# Step 3: Write the AS-based edges to a new CSV file using Pandas
as_df = []
label = 1
headers = ['From', 'To', 'domain', 'label']

for domain in paths:
    path = paths[domain]
    for i in range(1, len(path)):
        as_df.append([path[i-1], path[i], domain, label])

as_df = pd.DataFrame(as_df)
as_df.set_axis(headers, axis='columns', inplace=True)
#as_df.to_csv('as_edges.csv')

# Making a list of all unique AS numbers
as_numbers = {'Source'}
for domain in paths:
    path = paths[domain]
    for node in path: as_numbers.add(node)

as_numbers = pd.DataFrame(as_numbers)
#as_numbers.to_csv('as_numbers.csv')