from functions.outline_vpn.outline_vpn import OutlineVPN


def new_key(url, name=None):
    client = OutlineVPN(api_url=url)
    key = client.create_key(name)
    return key.key_id, key.access_url

def del_key(url, key_id):
    client = OutlineVPN(api_url=url)
    client.delete_key(key_id)