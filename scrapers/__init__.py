import json

def load_sources(sources_path):
    '''
    Load Scraping sources from assets/sources.json
    '''
    with open(sources_path, 'r') as file:
        sources = json.load(file)

    return sources

def rm_duplicates(sources_path):
    '''
    Check if there are duplicate sources in assets/sources.json and remove them
    '''
    
    with open(sources_path, 'r') as file:
        sources = json.load(file)

    duplicates = 0
    for key, values in sources.items():
        for value in values:
            if values.count(value) > 1:
                duplicates += 1

    if duplicates >= 1:
        # Remove duplicates
        for key in sources:
            sources[key] = list(set(sources[key]))
    
        # Save the updated unique sources back to the file
        with open(sources_path, 'w') as file:
            json.dump(sources, file, indent=2)
    
        print("[info] Removed",str(duplicates),"duplicates from sources.json")

sources_path = 'assets/sources.json'
rm_duplicates(sources_path)

# Load proxy settings
sources = load_sources(sources_path)

# Expose the proxy lists
http_proxy_list = sources["http"]
https_proxy_list = sources["https"]
socks4_proxy_list = sources["socks4"]
socks5_proxy_list = sources["socks5"]
