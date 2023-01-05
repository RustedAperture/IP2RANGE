# IP -> CIDR

This script will convert a csv list of IP addresses into their respective CIDR subnets with the owner names.

## output example

|    CIDR    |                   Owner                   |
|:----------:|:-----------------------------------------:|
| 8.0.0.0/9  |            Level 3 Parent, LLC            |
| 1.1.1.0/24 | APNIC and Cloudflare DNS Resolver project |
|            |                                           |

## Requirements

- Python3
- ipwhois
- tqdm
- netaddr
- ipaddress

## Usage

`Python3 IP2CIDR.py -f <input_file> -o <output_file>`