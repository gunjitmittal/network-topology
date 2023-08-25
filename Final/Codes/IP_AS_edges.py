import pandas as pd
from itertools import groupby
from pprint import pprint

# Step 1: Read ip.csv to create a mapping of IP addresses to AS numbers
ip_as_mapping = pd.read_csv('ip.csv')
ip_as_mapping = ip_as_mapping.iloc[:, :2]
ip_as_mapping = dict(ip_as_mapping.values)

# Step 2: Read out.csv and replace IP-based edges with AS-based edges
as_df = []

def as_org_split(s):
    if s is None: return None, None
    ls = s.split()
    return ls[0], ' '.join(ls[1:])

def fill(label):

    as_edges = []
    out_df = pd.read_csv('edges.csv')
    for _, row in out_df.iterrows():
        src_ip, dst_ip, domain, lab, ttl = row
        src_as = ip_as_mapping.get(src_ip)
        dst_as = ip_as_mapping.get(dst_ip)
        if label == lab: as_edges.append([src_as, dst_as, domain])

    paths = {}
    for edge in as_edges:
        if edge[2] not in paths: paths[edge[2]] = []
        if edge[0] is not None: paths[edge[2]].append(edge[0])
        if edge[1] is not None: paths[edge[2]].append(edge[1])

    for domain in paths:
        paths[domain] = [i[0] for i in groupby(paths[domain])]

    for domain in paths:
        path = paths[domain]
        for i in range(1, len(path)):
            as_df.append([path[i-1], path[i], domain, label])

for i in range(1, 5):
    fill(i)

# Making a list of all unique AS numbers
as_numbers_set = set()
for edge in as_df:
    as_numbers_set.add(edge[0])
    as_numbers_set.add(edge[1])

as_numbers = []
for as_number in as_numbers_set:
    asn, org = as_org_split(as_number)
    as_numbers.append([asn, org])

as_numbers = pd.DataFrame(as_numbers)
as_numbers.set_axis(['Label', 'Organization'], axis='columns', inplace=True)
as_numbers.to_csv('as_numbers.csv', index=False)

# Step 3: Write the AS-based edges to a new CSV file using Pandas
for i, edge in enumerate(as_df):
    asn1, org1 = as_org_split(edge[0])
    asn2, org2 = as_org_split(edge[1])
    as_df[i][0] = asn1
    as_df[i][1] = asn2

as_df = pd.DataFrame(as_df)
as_df.index += 1
as_df.set_axis(['From', 'To', 'Domain', 'Source'], axis='columns', inplace=True)
as_df.to_csv('as_edges_index.csv', index_label='id')

print(as_df)