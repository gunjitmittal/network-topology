
import requests,json
import pandas as pd

domains = [
    "google.com",
    "fitbit.com",
    "harvard.edu",
    "ngfix.fearp.usp.br",
    "kelso.ed.ac.uk",
    "facebook.com",
    "instagram.com",
    "delugerpg.com",
    "friv.com",
    "guinnessworldrecords.com",
    "miniclip.com",
    "notdoppler.com"
]

def get_data(ips):
    url = "http://ip-api.com/batch"
    final_data = []
    for i in range(0, len(ips), 100):
        chunk_ips =  ips[i:i + 100]
        response = requests.post(url, data=json.dumps(chunk_ips))
        data = json.loads(response.text)
        for ip in data:
            if(ip['status'] == 'fail'):
                continue
            if(ip['as']==''):
                continue
            final_data.append([ip['query'], ip['as'], str(ip['lat'])+','+str(ip['lon'])])
    return final_data


df=pd.read_csv("IP.csv")
df.to_numpy()
l=df['IP'].to_list()

conn=pd.read_csv('temp.csv')
as_N=pd.read_csv('AS.csv')

asips=as_N['IP'].to_list()

ips=[]
t=conn.to_numpy()
for i in range(len(t)):
    if t[i][0] not in ips and (t[0][2] in domains):
        ips.append(t[i][0])
    if t[i][1] not in ips and (t[0][2] in domains):
        ips.append(t[i][1])


df1=pd.DataFrame(ips,columns=['IP'])
df1.to_csv('IP.csv',index=False)

df2=pd.DataFrame(t,columns=['IP','AS','LOC'])
df2.to_csv('AS.csv',index=False)


a1=[]


for i in range(len(t)):
    if t[i][0] not in asips:
        a1.append(t[i][0])
    if t[i][1] not in asips:
        a1.append(t[i][1])

a1=list(set(a1))


i=0

unique_as=[]
as_path=[]
for curr in domains:
    path=['192.168.29.1']
    path1=[]
    for j in range(len(t)):
        if t[j][0] not in path and t[j][0] in asips and t[j][2]==curr:
            path.append(t[j][0])
        if t[j][1] not in path and t[j][1] in asips and t[j][2]==curr:
            path.append(t[j][1])
    
    for j in range(1,len(path)):
        a_0=as_N.loc[as_N['IP']==path[j],'AS'].item()
        if a_0 not in path1:
            path1.append(a_0)
    as_path.append([path1,curr])
    i+=1

print(as_path)

y=[]
for i in range(len(as_path)):
    prev='source-5'
    for j in range(len(as_path[i][0])):
        y.append([prev,as_path[i][0][j],as_path[i][1]])
        prev=as_path[i][0][j]

df3=pd.DataFrame(y,columns=['Source','Destination','Domain'])
df3.to_csv('Final_AS.csv',index=False)

df4=pd.read_csv("as_numbers.csv")
df5=pd.read_csv('temp2.csv')

p=df4['Label'].to_list()
q=df5['IP'].to_list()

p=['195.22.213.126','93.186.128.57','195.22.205.9']
for i in p:
    url=f"https://freeapi.dnslytics.net/v1/ip2asn/{i}"
    response=requests.get(url)
    print(response.json()['cidr'])

o=[]
for i in range(len(q)):
    url=f"https://freeapi.dnslytics.net/v1/ip2asn/{q[i]}"
    response=requests.get(url)
    o.append(response.json()['cidr'])



    

        



    



    


     



