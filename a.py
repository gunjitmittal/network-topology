import csv, requests, json

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
    
    
def parse_traceroute_data(data):
    traceroute_entries = data.strip().split("\n")
    traceroutes = {}
    current_traceroute = []
    key = traceroute_entries[0]
    for entry in traceroute_entries[1:]:
        if(len(entry.split()) == 1):
            if current_traceroute:
                traceroutes[key] = current_traceroute
                current_traceroute = []
                key = entry
        else:
            current_traceroute.append(entry)

    if current_traceroute:
        traceroutes[key] = current_traceroute

    return traceroutes

def main():
    input_files = ['a1.txt','b1.txt','c1.txt','ankit1.txt']
    output_files = ['out_1.csv', 'out1_1.csv', 'out2_1.csv', 'out3_1.csv']
    label = ['1','2','3','4']
    ips = []
    for p in range(0,4):
        with open(input_files[p], "r") as file:
            data = file.read()

        traceroutes = parse_traceroute_data(data)
        with open(output_files[p], "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["From", "To", "domain", "label", "TTL"])
        for key,traceroute in traceroutes.items():
            csv_filename = output_files[p]
            traceroute_rows = []
            begin = 0
            while(traceroute[begin].split()[1]=='*'):
                begin+=1
            previous_ip = traceroute[begin].split()[2].replace("(", "").replace(")","")
            ips.append(previous_ip)
            for i in range(1, len(traceroute)):
                parts = traceroute[i].split()
                if len(parts) >= 4:  # Adjusted to 4 for the correct data format
                    source_ip = previous_ip
                    dest_ip = parts[2].replace("(", "").replace(")","")  # Using the correct index
                    ips.append(dest_ip)
                    previous_ip = dest_ip
                    dest_domain = key
                    traceroute_rows.append([source_ip, dest_ip, dest_domain, label[p], parts[0]])

            with open(csv_filename, "a", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(traceroute_rows)

        print(f"CSV data for traceroute has been written to {csv_filename}")
    with open("ip1.csv", "w", newline="") as csv_file:
        csv.writer(csv_file).writerow(["IP", "label", "loc"])
        csv_writer = csv.writer(csv_file)
        ip_data = get_data(ips)
        for ip in ip_data:
            csv_writer.writerow(ip)

if __name__ == "__main__":
    main()
