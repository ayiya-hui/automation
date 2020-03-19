EXPECT='expect'
ACTUAL='actual'
NAME='name'
MISS='missing'
VALUE='value'
SEPERATOR='$SEPERATOR$'

class hashCompareHandler:
    def __init__(self, hash1, hash2, skip=False, ignore=False):
        self.hash1=hash1
        self.hash2=hash2
        if skip:
            self.skip=skip
        self.missKey1=[key for key in hash1.keys() if not hash2.has_key(key)]
        if ignore:
            self.missKey2=[key for key in hash2.keys() if not hash1.has_key(key) and key not in ignore]
        else:
            self.missKey2=[key for key in hash2.keys() if not hash1.has_key(key)]
        self.commKey=[key for key in hash1.keys() if  hash2.has_key(key)]
        self.missed=[]
        self.improved=[]
        self.passed=[]
        self.failed=[]

    def compareHash(self):
        if len(self.missKey1):
            self.__fillMiss()
        if len(self.missKey2):
            self.__fillImprove()
        if len(self.commKey):
            self.__fillComm()

        if len(self.failed):
            status='Fail'
        elif len(self.missed):
            status='Miss'
        elif len(self.improved):
            status='Improve'
        else:
            status='Pass'

        return status, self.passed, self.failed, self.missed, self.improved

    def __fillMiss(self):
        for key in self.missKey1:
            map={}
            map[NAME]=str(key)
            map[EXPECT]=str(self.hash1[key])
            map[ACTUAL]=MISS
            self.missed.append(map)

    def __fillImprove(self):
        for key in self.missKey2:
            map={}
            map[NAME]=str(key)
            map[EXPECT]=MISS
            map[ACTUAL]=str(self.hash2[key])
            self.improved.append(map)

    def __fillComm(self):
        for key in self.commKey:
            map={}
            map[NAME]=str(key)
            map[EXPECT]=str(self.hash1[key]).strip()
            if SEPERATOR in self.hash2[key]:
                v1, v2=self.hash2[key].split(SEPERATOR)
                if v2:
                    myValue=v2
                else:
                    myValue=v1
            else:
                myValue=self.hash2[key]
            map[ACTUAL]=str(myValue).strip()
            if map[EXPECT]==map[ACTUAL]:
                self.passed.append(map)
            elif self.skip and map[EXPECT]in self.skip:
                self.passed.append(map)
            else:
                self.failed.append(map)

def hashMethod(hashList):
    params={}
    for name in [NAME, EXPECT, ACTUAL]:
        myList=[hash[name] for hash in hashList]
        myStr=','.join(myList)
        params[name]=myStr
    return params

def hashMethod1(hashList):
    params={}
    for hash in hashList:
        name=hash[NAME]
        value=hash[VALUE]
        if name in params.keys():
            value=params[name]+SEPERATOR+value
        params[name]=value

    return params

def getHashKeys(hash1, hash2):
    missKey=[key for key in hash1.keys() if not hash2.has_key(key)]
    extraKey=[key for key in hash2.keys() if not hash1.has_key(key)]
    commKey=[key for key in hash1.keys() if  hash2.has_key(key)]

    return missKey, extraKey, commKey




