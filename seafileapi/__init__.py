from seafileapi.client import SeafileApiClient

def connect(server, username, password, debug=False):
    client = SeafileApiClient(server, username, password, None, debug)
    return client
