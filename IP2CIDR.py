from ipwhois import IPWhois
from tqdm import tqdm
import sys, getopt, csv, ipaddress, netaddr

def clean_list(list):
    newlist = []
    for a in list:
        newlist.append(a.__str__())

    return newlist

def get_owners(cidr_list):
    final_list = []

    pbar=tqdm(cidr_list)

    for x in pbar:
        pbar.set_description("Finding Owners")
        obj = IPWhois(x.split("/")[0])
        res = obj.lookup_whois()
        cidr_owner = check_owner(res)
        if cidr_owner == None:
            cidr_owner = check_name(res)
        final_list.append([x, cidr_owner])

    return final_list

def ip_list(file):
    results = []
    cidr_list = []
    current_cidr = "0.0.0.0/24"

    with open(file, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader: # each row is a list
            results.append(row)

    pbar = tqdm(results)

    for a in pbar:
        pbar.set_description("Finding CIDRs")
        for b in a:
            if ipaddress.ip_address(b) in ipaddress.ip_network(current_cidr):
                continue
            else:
                obj = IPWhois(str(b))
                res = obj.lookup_whois()
                current_cidr = check_cidr(res)
                if "," in current_cidr:
                    for l in current_cidr.split(","):
                        if l not in cidr_list:
                            cidr_list.append(l.strip())
                    current_cidr = "0.0.0.0/24"
                    continue
                if current_cidr not in cidr_list:
                    cidr_list.append(current_cidr)

    print("Merging Neighbor CIDRs.")
    summary = netaddr.cidr_merge(cidr_list)
    return get_owners(clean_list(summary))

def output_list(file, list):
    fields = ["CIDR", "Owner"]

    print("Outputting file.")

    with open(file, 'w+', newline='') as outfile:
        write = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        write.writerow(fields)
        write.writerows(list)

def check_cidr(res):
    return res["nets"][0]["cidr"]

def check_owner(res):
    return res["nets"][0]["description"]

def check_country(res):
    return res["nets"][0]["country"]

def check_name(res):
    return res["nets"][0]["name"]

def check(res):
    print("Owner:\t\t" + res["nets"][0]["description"])
    print("Country:\t" + res["nets"][0]["country"])
    print("CIDR:\t\t" + res["nets"][0]["cidr"])
    print("Range:\t\t" + res["nets"][0]["range"])

def main(argv):
    opts, args = getopt.getopt(argv,"hi:f:o:",["ip=", "input=", "output=", "cidr", "whois", "owner"])
    cidr_list = []
    ip_address = ""

    for opt, arg in opts:
        if opt == '-h':
            print ('ip2range.py -i <ip address> -f <csv list> -o <output csv> --cidr --whois --owner')
            sys.exit()
        elif opt in ("-i", "--ip"):
            ip_address = IPWhois(str(arg))
        elif opt in ("-f", "--input"):
            cidr_list = ip_list(arg)
        elif opt in ("-o", "--output"):
            output_list(arg, cidr_list)
        elif opt in ("--cidr"):
            print("CIDR:\t" + check_cidr(ip_address.lookup_whois()))
        elif opt in ("--whois"):
            check(ip_address.lookup_whois())
        elif opt in ("--owner"):
            print(check_owner(ip_address.lookup_whois()))
        
    
if __name__ == "__main__":
   main(sys.argv[1:])