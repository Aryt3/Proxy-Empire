import tomli

def load_config():
    '''
    Function to read and parse contents of pyproject.toml
    '''

    config = tomli.load(open("pyproject.toml", "rb"))
    
    return config.get("tool", {}).get("sources", {})

# Load proxy settings
proxy_config = load_config()

# Expose the proxy lists
http_proxy_list = proxy_config.get("http_proxy_list", [])
socks4_proxy_list = proxy_config.get("socks4_proxy_list", [])
socks5_proxy_list = proxy_config.get("socks5_proxy_list", [])
