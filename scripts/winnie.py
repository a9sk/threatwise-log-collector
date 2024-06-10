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

        trap['name'] = config[section]
        trap['modified_address'] = generate_address(config[section]['url'], config[section]['version'])
        trap['version'] = config[section]['version']
        trap['api_key'] = config[section]['key']
        trap['search_payload'] = json.loads(config[section]['payload'])

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
    mod_address = f"{parts[0]}-apl.{parts[1]}/api/v{version}"
    return mod_address

def make_post_request(url, payload):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def write_logs(logs, filename):

    # salvo tutto in un file json, questa parte penso che vada cambiata
    with open(filename, 'a') as file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"--------{timestamp}--------:\n {json.dumps(logs)}\n")

def save_file(file, filename):
    # il file si salva con url_data e ora.estensione
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    filename.split('.')
    filename = f"{filename[0]}{timestamp}.{filename[1]}"
    with open(filename, 'w') as f:
        f.write(file)

def save_logs(trap):

    # mi prendo i valori dalla singola trappola
    search_url = f"{trap['modified_address']}/events/search"

    search_response = make_post_request(search_url, trap['search_payload'])

    search_id = search_response.get("search_id")

    if search_id:
        pages = search_response.get("number_of_pages")

        for page in pages:
            show_payload = {
                "api_key": trap['api_key'],
                "search_id": search_id,
                "page": page
            }

            show_url = f"{trap['modified_address']}/events/show"
            
            show_response = make_post_request(show_url, show_payload)

            events = events + "\n" + show_response.get("events")

        write_logs(events, f"{trap['name']}-logs.json")

        # se la risposta alla search contiene file li scarico e li salvo
        if search_response["x_trapx_com_pcap"] == True:
            download_url = f"{trap['modified_address']}/events/download"
            download_payload = {
                "api_key": trap['api_key'],
                "event": search_response['x_Commvault Cloud_com_eventid'],
                "file": "pcap"
            }
            content= make_post_request(download_url, download_payload)
            save_file(content, f"{trap['name']}_.pcap")
        
        if search_id["x_trapx_com_binary"] == True:
            download_url = f"{trap['modified_address']}/events/download"
            download_payload = {
                "api_key": trap['api_key'],
                "event": search_response['x_Commvault Cloud_com_eventid'],
                "file": "binary"
            }
            content=  make_post_request(download_url, download_payload)
            # se il contenuto è binario vene salvato in uno zip, poi per aprire lo zip la password è MALICIOUS
            save_file(content, f"{trap['name']}_.zip")

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

    traps_data = initial_setup(filename)
    while True:
        main(traps_data)
        # fa un check ogni 10 minuti
        time.sleep(600)