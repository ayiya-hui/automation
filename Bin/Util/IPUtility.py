from IPy import IP

def combineIP(ipString, number):
    base_ip=IP(ipString).int()
    new_ip=IP(base_ip+number)

    return IP(new_ip).__str__()
