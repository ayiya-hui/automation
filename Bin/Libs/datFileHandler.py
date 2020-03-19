from Models.testConfigs import testData, testDataItem
import codecs

eventParsing_key='[reptDevIpAddr(key)]'

def getData(path, sections):
    """This method will read from dat file."""
    data=__readDatFile(path, sections)
    obj=testData()
    obj.path=path
    for key in data.keys():
        subobj=testDataItem()
        for subKey in data[key].keys():
            setattr(subobj, subKey, data[key][subKey])
        obj.dataMap[key]=subobj

    return obj

def __readDatFile(path, sections):
    data={}
    if 'mapKey' in sections.keys():
        mapKey=sections['mapKey']
    else:
        mapKey=None
        data['default']={}
    mapKeys=[]
    strKeys=[]
    for key in sections.keys():
        if key!='mapKey':
            if sections[key]=='map':
                mapKeys.append(key)
            elif sections[key]=='str':
                strKeys.append(key)
    lines=codecs.open(path, encoding='utf-8')
    keyword=''
    keyValue=''
    for line in lines:
        rawLine=line.strip()
        if rawLine:
            stripLine=rawLine.encode('ascii', 'ignore')
            t=stripLine[1:-1]
            if t in sections:
                keyword=t
            else:
                if mapKey:
                    if mapKey==keyword:
                        data[rawLine]={}
                        keyValue=rawLine
                    else:
                        if keyword in strKeys:
                            data[keyValue][keyword]=rawLine
                        elif keyword in mapKeys:
                            name, value=rawLine.split('=', 1)
                            if keyword in data[keyValue].keys():
                                myMap=data[keyValue][keyword]
                                myMap[name]=value
                                data[keyValue][keyword]=myMap
                            else:
                                data[keyValue][keyword]={}
                                data[keyValue][keyword][name]=value
                else:
                    if keyword in data['default'].keys():
                        data['default'][keyword].append(line)
                    else:
                        map=[stripLine]
                        data['default'][keyword]=map

    return data






