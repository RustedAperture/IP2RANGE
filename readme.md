# IP -> CIDR

This script will convert a csv list of IP addresses into their respective CIDR subnets with the owner names.

## output example

### Regular

|      CIDR       |
|:---------------:|
|    8.0.0.0/9    |
| 208.67.216.0/21 |

### Detailed

|      CIDR       |       Owner        | Country |
|:---------------:|:------------------:|:-------:|
|    8.0.0.0/9    | Level 3 Parent LLC |   US    |
| 208.67.216.0/21 | Cisco OpenDNS LLC  |   US    |

## Requirements

- Python3
- ipwhois
- tqdm
- netaddr
- ipaddress

## Usage

`Python3 IP2CIDR.py -i <input_file> -o <output_file>`

By adding the `--detail` option it will add the Country and owner to the CSV