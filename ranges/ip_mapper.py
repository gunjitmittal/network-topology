import pandas as pd
import requests, json
from pprint import pprint

ip_df = pd.read_csv('ip_test.csv')
ip_df = ip_df[['IP', 'label']]
ip_df.set_axis(['IP', 'AS'], axis=1, inplace=True)
ip_df['AS'] = ip_df['AS'].apply(lambda x: x.split()[0])
ip_df = ip_df.sort_values('AS')
#print(ip_df)

ips = ip_df['IP'].to_list()
asn = ip_df['AS'].to_list()

# ip_range = []

# for ip in ips:
#     url=f"https://freeapi.dnslytics.net/v1/ip2asn/{ip}"
#     response=requests.get(url)

#     if 'cidr' in response.json():
#         ip_range.append(response.json()['cidr'])
#     else:
#         ip_range.append(-1)

# ip_df['Range'] = ip_range
# print(ip_df)
# ip_df.to_csv('ip_ranges_as.csv', index=False)
# ================================================
# df=pd.DataFrame(ip_range,columns=['iprange'])
# df.to_csv('ip_ranges.csv',index=False)

ranges_df = pd.read_csv('ip_ranges_as.csv')
# ranges_ls = ranges_df['iprange'].tolist()
ranges_dict = {}

for id, row in ranges_df.iterrows():
    if row['AS'] not in ranges_dict:
        ranges_dict[row['AS']] = {row['Range']}
    else:
        ranges_dict[row['AS']].add(row['Range'])

# for i, r in enumerate(ranges_ls):
#     if r != '-12':
#         if asn[i] not in ranges_dict:
#             ranges_dict[asn[i]] = {r}
#         else:
#             ranges_dict[asn[i]].add(r)

# pprint(ranges_dict)
# print(len(ranges_dict))

df = []
for asn in ranges_dict:
    for r in ranges_dict[asn]:
        df.append([asn, r])

df = pd.DataFrame(df, columns=['AS', 'Range'])
print(df)
df.to_csv('ip_ranges_final.csv', index=False)