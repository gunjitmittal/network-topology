import csv, requests, json
ips = []

def get_data(ip):
    url = "http://ip-api.com/json/" + ip
    response = requests.get(url)
    data = json.loads(response.text)
    if(data['status'] == 'fail'):
        return None
    return [ip, data['as'], str(data['lat'])+','+str(data['lon'])]
    

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
    with open("ankit1.txt", "r") as file:
        data = file.read()

    traceroutes = parse_traceroute_data(data)
    with open("out3_1.csv", "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["From", "To", "domain", "label", "TTL"])
    for key,traceroute in traceroutes.items():
        csv_filename = "out3_1.csv"
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
                traceroute_rows.append([source_ip, dest_ip, dest_domain, '4', parts[0]])

        with open(csv_filename, "a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(traceroute_rows)

    print(f"CSV data for traceroute has been written to {csv_filename}")
    for ip in ips:
        with open("ip.csv", "a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            if(get_data(ip) != None):
                csv_writer.writerow(get_data(ip))

if __name__ == "__main__":
    main()
