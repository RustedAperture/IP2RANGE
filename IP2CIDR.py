from ipwhois import IPWhois
from tqdm import tqdm
import sys, getopt, csv, ipaddress, netaddr

def clean_list(list):
    # Clean the list to remove the IPNetwork tag from CIDR_merge
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
        res = obj.lookup_whois() # Perform lookup of CIDR IP

        cidr_owner = check_owner(res) # Lookup owner information
        if cidr_owner == None: cidr_owner = check_name(res) # Replace with name if no description
        x.append(cidr_owner) # Add owner information
    
        cidr_country = check_country(res) # Lookup country information
        x.append(cidr_country) # Add country information

        final_list.append(x)

    return final_list

def input_list(file, opts):
    input_ip_list = []
    cidr_list = []
    current_cidr = "0.0.0.0/24"

    with open(file, mode='r', encoding='utf-8-sig') as csvfile: # Open file and create a list
        reader = csv.reader(csvfile)
        for row in reader: input_ip_list.append(row)

    pbar = tqdm(input_ip_list)

    for a in pbar:
        pbar.set_description("Finding CIDRs")
        for b in a:
            if ipaddress.ip_address(b) in ipaddress.ip_network(current_cidr): continue # Check if IP is in range, if so skip to next IP address
            else:
                obj = IPWhois(str(b)) 
                res = obj.lookup_whois() # Perform lookup of IP from list
                current_cidr = check_cidr(res)

                if "," in current_cidr: # Setup logic to handle comma seperated CIDR
                    for l in current_cidr.split(","): # Split the comma list into multiple CIDR
                        if l not in cidr_list:
                            cidr_list.append(l.strip()) # Add the CIDR to the list
                    current_cidr = "0.0.0.0/24" # Reset the current CIDR to prevent crash
                    continue # Skip to next CIDR

                if current_cidr not in cidr_list:cidr_list.append(current_cidr) # If not in the list add it

    print("Merging Neighbor CIDRs.")

    summary = clean_list(netaddr.cidr_merge(cidr_list)) # Clean the list to remove the IPNetwork tag from CIDR_merge

    return get_additional(summary) if ('--detail', '') in opts else summary

def output_list(file, list, opts):
    fields = ["CIDR"]

    if ('--detail', '') in opts: 
        fields.append("Owner")
        fields.append("Country")

    print("Outputting file.")

    with open(file, 'w+', newline='') as outfile:

        for i in fields: outfile.write('"%s",' % i) # Add the fields to the file
        outfile.write("\n") 
        
        for i in list:
            for x in i: outfile.write('"%s",' % x) # Add the CIDR info
            outfile.write("\n")

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
        elif opt in ("-i", "--input"): cidr_list = input_list(arg, opts)
        elif opt in ("-o", "--output"): output_list(arg, cidr_list, opts)
        
    
if __name__ == "__main__":
   main(sys.argv[1:])