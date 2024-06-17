import requests
import sys
import time
import json
import configparser
import json

# variabili globali
traps_data = ""

def initial_setup(filename):
    # file ini per la configurazione contenente tutte le robe che servono

    # lista di dizionari per tenere la configurazione
    config = configparser.ConfigParser()
    config.read(filename)

    traps = []

    for section in config.sections():
        trap = {} 
        TEMP = json.loads(config[section]["filter"])
        trap['name'] = f"{TEMP.get('trap_name')}-{TEMP.get('department')}"
        #print(f"[debug] name: {trap['name']}")
        trap['modified_address'] = generate_address(config[section]['url'], config[section]['version'])
        #print(f"[debug] address: {trap['modified_address']}")
        trap['version'] = config[section]['version']
        #print(f"[debug] version: {trap['version']}")
        trap['api_key'] = config[section]['key']
        #print(f"[debug] api key: {trap['api_key']}")
        trap['search_payload'] = json.loads(config[section]['filter'].replace("'", '"'))
        #print(f"[debug] payload: {trap['search_payload']}")
        print(trap)
        traps.append(trap)

    return traps

def usage():
    print("""Usage: 

python3 script.py -f <PATH/filename>

Use the flag -f to insert the .ini configuration file.
    """)
    exit()
    
def generate_address(url, version):
    # prendo la versione della trappola
    parts = url.split('.')
    mod_address = f"{parts[0]}-apl.threatwise.metallic.io:8443/api/v{version}"
    return mod_address

def make_post_request(url, payload):
    response = requests.post(url, json=payload)
    # print(f"{response.text}\n\n\n")
    return response

def write_logs(logs, filename):
    # salvo tutto in un file json, questa parte penso che vada cambiata
    with open(filename, 'a') as file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        file.write(f'"time":"{timestamp}"\n {json.dumps(logs)}\n')

def save_file(file, filename):
    # il file si salva con url_data e ora.estensione
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    parts= filename.split('.')
    filename = f"{parts[0]}_{timestamp}.{parts[1]}"
    # print(file.text)
    with open(filename, 'wb') as f:
        f.write(file.encode('Utf-8'))

def save_logs(trap):

    search_payload = {
        "api_key":f"{trap['api_key']}",
        "filter": trap['payload']
    }
    # mi prendo i valori dalla singola trappola
    search_url = f"{trap['modified_address']}/events/search"

    search_response = make_post_request(search_url, search_payload)

    search_id = search_response.get("search_id")

    if search_id:
        events=[]
        pages = search_response.get("number_of_pages")
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
        
        write_logs(events, f"{trap['name']}-logs.json")

        for event in events:
            # se la risposta alla search contiene file li scarico e li salvo
            if event.get("x_trapx_com_pcap") == True:
                print(f"[!] Looks like there is a .pcap file in the event with id: {event.get('x_trapx_com_eventid')}")
                # download_url = f"{trap['modified_address']}/events/download"
                # download_payload = {
                #     "api_key": trap['api_key'],
                #     "event_id": f"{event.get('x_trapx_com_eventid')}",
                #     "file": "pcap"
                # }
                # content = make_post_request(download_url, download_payload)
                # save_file(content, f"{trap['name']}_{event.get('x_trapx_com_eventid')}.zip")
            
            if event.get("x_trapx_com_binary") == True:
                print(f"[!] Looks like there is a binary file in the event with id: {event.get('x_trapx_com_eventid')}")
                # download_url = f"{trap['modified_address']}/events/download"
                # download_payload = {
                #     "api_key": trap['api_key'],
                #     "event_id": f"{event.get('x_trapx_com_eventid')}",
                #     "file": "binary"
                # }
                # content=  make_post_request(download_url, download_payload)
                # save_file(content, f"{trap['name']}_{event.get('x_trapx_com_eventid')}.zip")

            # cancel_payload = {
            # "api_key":f"{trap['api_key']}",
            # "search_id": search_id
            # }
            # cancel_url = f"{trap['modified_address']}/events/cancel"
            # cancel_response = make_post_request(cancel_url, cancel_payload)
            # print(cancel_response)

            delete_payload = {
            "api_key":f"{trap['api_key']}",
            "search_id": search_id
            }
            delete_url = f"{trap['modified_address']}/events/delete"
            make_post_request(delete_url, delete_payload)

    else:
        print("[!] No search_id was found in the response")

def main(traps):
    # salvo i log per ogni nodo della lista
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
    except KeyboardInterrupt:
        print("[!] Keyboad Interrupt detected, exiting...")
        exit
    
    while True:
        try:
            main(traps_data)
            # fa un check ogni 10 minuti
            print("[...] Waiting...")
            time.sleep(600)
        except KeyboardInterrupt:
            print("[!] Keyboad Interrupt detected, exiting...")
            exit()