import requests
import sys
import time
import json
import configparser
import json

# -------------------
# Global Variables

traps_data = ""

def initial_setup(filename):
    # -----NEEDS-----
    # File ini for the configuration

    # -----USES-----
    # List of dicts to keep the trap's configurations 

    config = configparser.ConfigParser()
    config.read(filename)

    traps = []

    # -------------------
    # Iterate through the config file and load it  

    for section in config.sections():
        trap = {} 
        TEMP = json.loads(config[section]["filter"])
        trap['name'] = f"{TEMP.get('trap_name')}-{TEMP.get('department')}"
        trap['modified_address'] = generate_address(config[section]['url'], config[section]['version'])
        trap['version'] = config[section]['version']
        trap['api_key'] = config[section]['key']
        trap['payload'] = json.loads(config[section]['filter'].replace("'", '"'))

        #  -------DEBUG------
        # Commands usefull for debugging

        # print(f"[debug] Name: {trap['name']}")
        # print(f"[debug] Address: {trap['modified_address']}")
        # print(f"[debug] Payload: {trap['search_payload']}")
        # print(f"[debug] Version: {trap['version']}")
        # print(f"[debug] Api Key: {trap['api_key']}")
        # print(f"[debug] Trap: {trap}")

        traps.append(trap)

    return traps

def usage():
    print("""Usage: 

python3 logs.py -f <PATH/filename>

Use the flag -f to insert the .ini configuration file.
    """)
    exit()
    
def generate_address(url, version):
    # -------------------
    # The API uses port 8443 for https API communication, you might want to add some policy for that on your firewall 

    parts = url.split('.')
    mod_address = f"{parts[0]}-apl.threatwise.metallic.io:8443/api/v{version}"
    return mod_address

def write_logs(logs, filename):
    # -------------------
    # Save everything in a json file

    with open(filename, 'a') as file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        file.write(f'"time":"{timestamp}"\n {json.dumps(logs)}\n')

def make_post_request(url, payload):
    # -------------------
    # Post requests are all made from this same function

    response = requests.post(url, json=payload)

    #  -------DEBUG------
    # Commands usefull for debugging

    # print(f"[debug] Response: {response.text}\n")

    return response

def save_file(file, filename):
    # -------------------
    # The file is saved using the timestamp and some other characteristics to make it unique

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    parts= filename.split('.')
    filename = f"{parts[0]}_{timestamp}.{parts[1]}"

    #  -------DEBUG------
    # Commands usefull for debugging    

    # print(f"[debug] Content: {file.text}")

    with open(filename, 'wb') as f:
        f.write(file.text.encode('Utf-8'))

def save_logs(trap):

    search_payload = {
        "api_key":f"{trap['api_key']}",
        "filter": trap['payload']
    }

    #  -------DEBUG------
    # Commands usefull for debugging
    
    # print(f"[debug] Search Payload: {search_payload})

    # -------------------
    # This takes the values for a sigle trap per iteration

    search_url = f"{trap['modified_address']}/events/search"

    search_response = make_post_request(search_url, search_payload).json()

    search_id = search_response.get("search_id")

    #  -------DEBUG------
    # Commands usefull for debugging

    # print(f"[debug] Search ID: {search_id})

    if search_id:
        events=[]
        pages = search_response.get("number_of_pages")

        # -------------------
        # If the response has multiple pages we will need to iterate throught all of them

        if pages:
            for page in pages:
                show_payload = {
                    "api_key": f"{trap['api_key']}",
                    "search_id": search_id,
                    "page": page,
                    "filter": f"{trap['payload']}"
                }
                show_url = f"{trap['modified_address']}/events/show"
                show_response = make_post_request(show_url, show_payload).json()
                events.extend(show_response.get("events", []))
        else:
            show_payload = {
                    "api_key": f"{trap['api_key']}",
                    "search_id": search_id,
                    "page": 1,
                    "filter": f"{trap['payload']}"
            }
            show_url = f"{trap['modified_address']}/events/show"
            
            show_response = make_post_request(show_url, show_payload).json()

            events.extend(show_response.get("events", []))
    
        # -------------------
        # Save the logs always in the same file (every trap should have its own)

        write_logs(events, f"{trap['name']}-logs.json")

        # -------------------
        # Iterate trought the events in the response and download eventual files (the downloads are disabled, to enable them remove the # sign)

        for event in events:

            if event.get("x_trapx_com_pcap") == True:
                
                #  -------DEBUG------
                # Commands usefull for debugging    

                print(f"[debug] Looks like there is a .pcap file in the event with id: {event.get('x_trapx_com_eventid')}")

                # -------------------
                # Actual code for downloading the file

                # download_url = f"{trap['modified_address']}/events/download"
                # download_payload = {
                #     "api_key": trap['api_key'],
                #     "event_id": f"{event.get('x_trapx_com_eventid')}",
                #     "file": "pcap"
                # }
                # content = make_post_request(download_url, download_payload)
                # save_file(content, f"{trap['name']}_{event.get('x_trapx_com_eventid')}.pcap")
        
            if event.get("x_trapx_com_binary") == True:
                                
                #  -------DEBUG------
                # Commands usefull for debugging  

                print(f"[!] Looks like there is a binary file in the event with id: {event.get('x_trapx_com_eventid')}")

                # -------------------
                # Actual code for downloading the file

                # download_url = f"{trap['modified_address']}/events/download"
                # download_payload = {
                #     "api_key": trap['api_key'],
                #     "event_id": f"{event.get('x_trapx_com_eventid')}",
                #     "file": "binary"
                # }
                # content=  make_post_request(download_url, download_payload)
                # save_file(content, f"{trap['name']}_{event.get('x_trapx_com_eventid')}.zip")

        # -------------------
        # Cancel logs from the TSOC's cache (default is commented, you might want to enable this)

        # cancel_payload = {
        # "api_key":f"{trap['api_key']}",
        # "search_id": search_id
        # }
        # cancel_url = f"{trap['modified_address']}/events/cancel"
        # cancel_response = make_post_request(cancel_url, cancel_payload)
        
        # -------------------
        # Delete logs so that they are not repeated in the next scan (do not disable this)

        delete_payload = {
        "api_key":f"{trap['api_key']}",
        "search_id": search_id
        }
        delete_url = f"{trap['modified_address']}/events/delete"
        make_post_request(delete_url, delete_payload)

    else:
        #  -------DEBUG------
        # Commands usefull for debugging

        print("[!] No search_id was found in the response")

def main(traps):
    for trap in traps:
        save_logs(trap)

if __name__ == "__main__":
    if(len(sys.argv)<2):
        usage()

    args = sys.argv[1:]

    if args[0]!='-f':
        usage()
    else:
        filename=args[1]
    try:
        traps_data = initial_setup(filename)
        #  -------DEBUG------
        # Commands usefull for debugging

        # print(f"[debug] {traps_data}")
    except KeyboardInterrupt:
        print("[!] Keyboad Interrupt detected, exiting...")
        exit
    
    while True:
        try:
            main(traps_data)
            # -------------------
            # Does a check every x time (defaut 600 seconds)

            print("[...] Waiting...")
            time.sleep(600)
        except KeyboardInterrupt:
            print("[!] Keyboad Interrupt detected, exiting...")
            exit()
        
        