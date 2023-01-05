# IP -> CIDR

This script will convert a csv list of IP addresses into their respective CIDR subnets with the owner names.

## Screenshots
![Screenshot of app running in WSL2](img/screenshot.png "App Running")
### Input Example
![Screenshot of input example](img/input.png "input example")
### Output Example
#### Regular
![simple output example](img/output_simple.png "simple output example")
#### Detailed
![detailed output example](img/output.png "detailed output example")

## Requirements

- Python3
- ipwhois
- tqdm
- netaddr
- ipaddress

## Usage & "Installation"

Instructions for Ubuntu
```
sudo apt install python3 python3-pip
pip3 install ipwhois tqdm netaddr ipaddress

git clone https://github.com/RustedAperture/IP2RANGE
cd IP2RANGE
Python3 IP2CIDR.py -i <input_file> -o <output_file> --detail
```

By adding the `--detail` option it will add the country and owner to the CSV
