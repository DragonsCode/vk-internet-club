from outline_vpn.outline_vpn import OutlineVPN


def new_key(url):
    client = OutlineVPN(api_url=url)
    key = client.create_key()
    return key.key_id

def del_key(url, key_id):
    client = OutlineVPN(api_url=url)
    client.delete_key(new_key.key_id)