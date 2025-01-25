import json

def load_config():
    '''
    Function to read and parse contents of pyproject.toml
    '''
    
    return json.load(open("assets/sources.jsonc", "r")) 

# Load proxy settings
proxy_config = load_config()

# Expose the proxy lists
http_proxy_list = proxy_config.get("http", [])
socks4_proxy_list = proxy_config.get("socks4", [])
socks5_proxy_list = proxy_config.get("socks5", [])
