from ipwhois import IPWhois
from tqdm import tqdm
import sys, getopt, csv, ipaddress, netaddr

def clean_list(list):
    newlist = []
    for a in list:
        newlist.append([a.__str__()])

    return newlist

def get_additional(cidr_list):
    final_list = []

    pbar = tqdm(cidr_list)

    for x in pbar:
        pbar.set_description("Getting Additional Info")
        obj = IPWhois(x[0].split("/")[0])
        res = obj.lookup_whois()

        cidr_owner = check_owner(res)
        if cidr_owner == None:
            cidr_owner = check_name(res)
        x.append(cidr_owner)
    
        cidr_country = check_country(res)
        x.append(cidr_country)

        final_list.append(x)

    return final_list

def ip_list(file, opts):
    results = []
    cidr_list = []
    current_cidr = "0.0.0.0/24"

    with open(file, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            results.append(row)

    pbar = tqdm(results)

    for a in pbar:
        pbar.set_description("Finding CIDRs")
        for b in a:
            if ipaddress.ip_address(b) in ipaddress.ip_network(current_cidr): continue
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
    return get_additional(clean_list(summary)) if ('--detail', '') in opts else clean_list(summary)

def output_list(file, list, opts):
    fields = ["CIDR"]

    if ('--detail', '') in opts: 
        fields.append("Owner")
        fields.append("Country")

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

def main(argv):
    opts, args = getopt.getopt(argv,"hi:o:",["input=", "output=", "detail"])
    cidr_list = []

    for opt, arg in opts:
        if opt == '-h':
            print ('ip2range.py -i <csv list> -o <output csv> --detail')
            sys.exit()
        elif opt in ("-i", "--input"):
            cidr_list = ip_list(arg, opts)
        elif opt in ("-o", "--output"):
            output_list(arg, cidr_list, opts)
        
    
if __name__ == "__main__":
   main(sys.argv[1:])