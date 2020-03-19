import random

def getRandomIPAddr():
	ips=[]
	for i in range(4):
		ips.append(str(int(random.randrange(1, 254))))

	return '.'.join(ips)

def getIpRandomFromList(ipList):
	num=int(random.randrange(0, len(ipList)))
	ip=ipList[num]
	return ip

def getRandomPort():
	return int(random.randrange(1000, 65535))

def getRandomNum(num1, num2):
	return str(random.randrange(num1, num2))

def getRandomDecimal(num1, num2):
	return str(random.randrange(num1, num2))+'.'+str(random.randrange(0, 100))

def getRandomMac():
	pick=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
	mac=[]
	for i in range(6):
		a=pick[random.randrange(0, len(pick))]
		b=pick[random.randrange(0, len(pick))]
		myStr=a+b
		mac.append(myStr)

	return ':'.join(mac)
