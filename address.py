import re
import sys

def print_usage():
    print("Usage: python address.py [-v <version>] [-r <resource>] <address>")

args = sys.argv[1:]
version = "1.60"  # default version
resource = ""

while args:
    arg = args.pop(0)
    if arg == "-v":
        if args:
            version = args.pop(0)
        else:
            print("Option -v requires an argument.")
            print_usage()
            sys.exit(1)
    elif arg == "-r":
        if args:
            resource = args.pop(0)
        else:
            print("Option -r requires an argument.")
            print_usage()
            sys.exit(1)
    elif re.match(r'^https?://.*', arg):
        address = arg
    else:
        print("Invalid option:", arg)
        print_usage()
        sys.exit(1)

if 'address' not in locals():
    address = input("Enter the address: ")

matches = re.match(r'^https?://([^./]+)\.(.+\.metallic\.io)/', address)
if matches:
    hostname = matches.group(1)
    domain = matches.group(2)
else:
    print("Invalid address format.")
    sys.exit(1)

modified_address = f"{hostname}-apl.{domain}/api/v{version}/{resource}"

print("Modified address:")
print(modified_address)
