import argparse
import json
import subprocess
from datetime import datetime

def save_to_file(output, file_path):
    with open(file_path, 'w') as f:
        json.dump(output, f)

def main():
    parser = argparse.ArgumentParser(description='Wrapper for Project Discovery tools')
    
    parser.add_argument('--target', '-t', required=False, help='Target domain or IP address')
    parser.add_argument('--list', '-l', required=False, help='Target domain or IP address')
    parser.add_argument('--naabu', '-n', action='store_true', help='Run naabu scan')
    parser.add_argument('--httpx', '-x', action='store_true', help='Run httpx scan')
    parser.add_argument('--nuclei', '-nu', action='store_true', help='Run nuclei scan')
    parser.add_argument('--chaos', '-c', action='store_true', help='Run chaos scan')
    parser.add_argument('--dnsx', '-d', action='store_true', help='Run dnsx scan')
    parser.add_argument('--subfinder', '-s', action='store_true', help='Run subfinder scan')
    parser.add_argument('--ports', '-p', nargs='+', default=[], help='Ports to scan (default: all ports)')
    parser.add_argument('--output', '-o', help='Output file path')

    args = parser.parse_args()

    if args.naabu:
        print('[*] Running naabu...')
        ports = ','.join(args.ports) if args.ports else '-'
        output = subprocess.run(['naabu', '-host', args.target, '-p', ports], stdout=subprocess.PIPE).stdout.decode().splitlines()
        if args.output:
            save_to_file(output, args.output + "_" + datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '.json')
        else:
            print('\n'.join(output))

# seems to be working
# need to add the switches for status codes, ip, tech
    if args.httpx:
        print('[*] Running httpx...')
        ports = ','.join(args.ports) if args.ports else '80,443'
        output = subprocess.run(['httpx', '-l', args.list, '-sc','-ip','-td','-ports', ports], stdout=subprocess.PIPE).stdout.decode().splitlines()
        if args.output:
            save_to_file(output, args.output + "_" + datetime.now().strftime("%Y_%m_%d-%I_%M_%S") +'.json')
        else:
            print('\n'.join(output))

# '-t','nuclei-templates/',

# this seems to work
# i can probably clean it up to work better though
    if args.nuclei:
        print('[*] Running nuclei...')
        output = subprocess.run(['nuclei', '-u', args.target], stdout=subprocess.PIPE).stdout.decode().splitlines()
        if args.output:
            save_to_file(output, args.output + "_" + datetime.now().strftime("%Y_%m_%d-%I_%M_%S") +'.json')
        else:
            print('\n'.join(output))

# seems to be good to go
    if args.chaos:
        print('[*] Running chaos...')
        output = subprocess.run(['chaos-client', '-d', args.target], stdout=subprocess.PIPE).stdout.decode().splitlines()
        if args.output:
            save_to_file(output, args.output + "_" + datetime.now().strftime("%Y_%m_%d-%I_%M_%S") +'.json')
        else:
            print('\n'.join(output))


# need to add the wordlist flag
    if args.dnsx:
        print('[*] Running dnsx...')
        output = subprocess.run(['dnsx', '-silent', '-a', '-cname', '-resp','-l', args.list], stdout=subprocess.PIPE).stdout.decode().splitlines()
        if args.output:
            save_to_file(output, args.output + "_" + datetime.now().strftime("%Y_%m_%d-%I_%M_%S") +'.json')
        else:
            print('\n'.join(output))

# seems to be working
# need to add ability to use some of the specialized switches
    if args.subfinder:
        print('[*] Running subfinder...')
        output = subprocess.run(['subfinder','-d', args.target], stdout=subprocess.PIPE).stdout.decode().splitlines()
        if args.output:
            save_to_file(output, args.output + "_" + datetime.now().strftime("%Y_%m_%d-%I_%M_%S") +'.json')
        else:
            print('\n'.join(output))

if __name__ == '__main__':
    main()