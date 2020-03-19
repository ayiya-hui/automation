from restApiDataHandler import restApiDataHandler
from caseDbHandler import caseDbHandler
from ConfigConstants.checkParseTemplate import html_content, table_body, table_row
from ConfigConstants.eventTypeTemplate import event_html_content, event_table_row
from string import Template
import re, os
from Util.localhostIp import getLocalhostIp
from Util.testUtility import processList

ignores=['PHBoxParser', 'PHRuleIncidentParser', 'SyslogNGParser']
summary_path='../Public/checkNewParsers.html'
event_reg={'set':'\<setEventAttribute attr=\"eventType\"\>%s\</setEventAttribute\>',
           'when':'\<when test=[\\\"\\\']\$eventType = [\\\'\\\"]%s[\\\'\\\"][\\\'\\\"]\>',
           'whenin':'\<when test=[\\\"\\\']\$eventType IN [\\\"\\\']%s[\\\"\\\'][\\\"\\\']\>'}
test_event_reg='\<testEvent\>\<!\[CDATA\[(?P<test>.*)\]\]\>\</testEvent\>'
all='[^\%s]+'
type='(?P<type>[^\%s]+)'
wildcard={'set':'<', 'when':'"\\\'', 'whenin':'"\\\''}
combined='combineMsgId'
result_path='../Public/parsersInfo'
pat_combined=re.compile(combined+'\((?P<msg>[^\)]+)\)')
pat_test_event=re.compile(test_event_reg)

class parserHandler:
    def __init__(self, appServer):
        self.rest=restApiDataHandler(appServer)
        self.parsers={}
        self.parser_names={}
        if not os.path.exists(result_path):
            os.mkdir(result_path)
        self.localhost=getLocalhostIp()
        self.dbHandler=caseDbHandler('EventParsing')
        self.needCoverEvents=[]
        self.testEvents=[]

    def checkNew(self, sysdefine=False):
        if not self.parser_names:
            self.getAllParserNames()
        exist_modules=[]
        new_modules=[]
        modules=self.dbHandler.getAllModules()
        for key in self.parser_names.keys():
            if not key in ignores:
                if not key.replace('Parser', '') in modules:
                    print 'New parser %s' % key
                    new_modules.append(key)
                else:
                    exist_modules.append(key)
        self.checkParserEvents(sys_define=sysdefine)
        self.createSummaryHtml(exist_modules, new_modules)
        self.saveNeedCoverEvents()
        self.saveTestEvents()

    def checkParserEvents(self, sys_define=False):
        event_map=self.getAllParserEvents(sysdefine=sys_define)
        for key in event_map.keys():
            ao_list=event_map[key]
            self.dbHandler.getEventTypesInModule(key.replace('Parser', ''))
            auto_list=self.dbHandler.module_event_map.keys()
            new_list, extra, exist_list=processList(ao_list, auto_list)
            new_wild_list=[]
            for item in new_list:
                if '$' in item:
                    new_wild_list.append(item)
                else:
                    self.needCoverEvents.append(item)
            if len(new_wild_list) and len(extra):
                for item in new_wild_list:
                    start_pos=item.find('$')
                    end_pos=start_pos+8
                    front=item[:start_pos]
                    end=item[end_pos+1:]
                    for e in extra:
                        if front==e[:start_pos] and end==e[end_pos+1:]:
                            exist_list.append(item)
                            new_list.remove(item)
                            extra.remove(e)
                            break
            print 'module name %s' % key
            self.createModuleHtml(key, exist_list, new_list)

    def getAllParserNames(self):
        self.parser_names=self.rest.getData('parsers', module='device')

    def getAllParsers(self, sys=False):
        self.parsers=self.rest.getData('eventParser')
        for i in ignores:
            self.parsers.pop(i)
        if sys:
            for key in self.parsers.keys():
                if self.parsers[key].attribute['sysDefined']!='true':
                    self.parsers.pop(key)

    def getParserEvents(self, parser_name, sysdefine=False):
        if not self.parsers:
            self.getAllParsers(sys=sysdefine)
        if not parser_name in self.parsers.keys():
            print 'No parser name %s exist.' % parser_name
        else:
            events=[]
            parser=self.parsers['parser_name']
            eventtype_list=parser.getEventTypes()

        return event_list

    def getAllParserEvents(self, sysdefine=False):
        event_types={}
        if not self.parsers:
            self.getAllParsers(sys=sysdefine)
        for parser in self.parsers.keys():
            events=[]
            eventtype_list=self.getEventTypes(self.parsers[parser])
            if parser not in event_types.keys():
                event_types[parser]=eventtype_list

        return event_types

    def getEventTypes(self, parser):
        type_list=[]
        find_map={}
        for key in event_reg.keys():
            pat_all=re.compile(event_reg[key] % (all % wildcard[key]))
            raw=pat_all.findall(parser.parserXml)
            if raw:
                find_map[key]=raw
        self.getTestEvent(parser.parserXml)
        if len(find_map):
            for key in find_map.keys():
                pat_type=re.compile(event_reg[key] % (type % wildcard[key]))
                for item in find_map[key]:
                    match=pat_type.match(item)
                    if match:
                        groups=match.groupdict()
                        type_name=groups['type']
                        type_temp=[]
                        if type_name.startswith(combined):
                            type_temp.append(type_name)
                        else:
                            type_temp=type_name.split(', ')
                        if len(type_temp):
                            for t in type_temp:
                                if t not in type_list:
                                    if t.startswith(combined):
                                        final_name=self.handleCombine(t)
                                    else:
                                        final_name=t
                                    type_list.append(final_name.strip('"'))

        return type_list

    def getTestEvent(self, xml):
        find_all=pat_test_event.findall(xml)
        self.testEvents.extend(find_all)

    def handleCombine(self, msg):
        name=''
        match=pat_combined.match(msg)
        if match:
            groups=match.groupdict()
            msg=groups['msg']
            temp=msg.split(',')
            new_temp=[]
            for i in temp:
                i=i.strip()
                if '"' in i:
                    new_temp.append(i.replace('"', ''))
                elif i.startswith('$'):
                    new_temp.append('$variable')
                else:
                    new_temp.append(i)
            name=''.join(new_temp)

        return name

    def createModuleHtml(self, name, exist, new):
        full_path=result_path+'/'+name+'.html'
        self.createHtml(exist, new, row=event_table_row, content=event_html_content, output=full_path, module_name=name)

    def createSummaryHtml(self, exist_modules, new_modules):
        self.createHtml(exist_modules, new_modules, row=table_row, content=html_content, url=True, output=summary_path)

    def createHtml(self, exist_modules, new_modules, row='', body=table_body, content='', url=False, output='', module_name=''):
        myRowTemp=Template(row)
        myTableTemp=Template(body)
        myHtmlTemp=Template(content)
        old_body=''
        new_body=''
        total_count=0
        old_count=0
        new_count=0
        if exist_modules:
            myRows=[]
            for key in exist_modules:
                myMap={'module':key}
                if url:
                    full_url=result_path.replace('../Public','http://'+self.localhost)+'/'+key+'.html'
                    myMap['url']=full_url
                myRows.append(myRowTemp.substitute(myMap))
            if myRows:
                oldMap={'tableBody':''.join(myRows)}
                old_body=myTableTemp.substitute(oldMap)
                old_count=len(myRows)
        if new_modules:
            newRows=[]
            for key in new_modules:
                myMap={'module':key}
                if url:
                    full_url=result_path.replace('../Public','http://'+self.localhost)+'/'+key+'.html'
                    myMap['url']=full_url
                newRows.append(myRowTemp.substitute(myMap))
            if newRows:
                newMap={'tableBody':''.join(newRows)}
                new_body=myTableTemp.substitute(newMap)
                new_count=len(newRows)
        htmlMap={}
        htmlMap['old']=old_body
        htmlMap['old_count']=old_count
        htmlMap['new']=new_body
        htmlMap['new_count']=new_count
        htmlMap['count']=old_count+new_count
        if not url:
            htmlMap['module_name']=module_name
        if htmlMap:
            final=myHtmlTemp.substitute((htmlMap))
            myW=open(output, 'w')
            myW.write(final)
            myW.close()

    def saveNeedCoverEvents(self):
        return self.__saveStuff(self.needCoverEvents, result_path+'/needCover.dat')

    def openNeedCoverEvents(self):
        self.needCoverEvents=self.__openStuff(result_path+'/needCover.dat')

    def saveTestEvents(self):
        return self.__saveStuff(self.testEvents, result_path+'/testEvents.dat')

    def openTestEvents(self):
        self.testEvents=self.__openStuff(result_path+'/testEvents.dat')

    def __saveStuff(self, data, path):
        myF=open(path, 'w')
        for e in data:
            myF.write(e+'\n')
        myF.close()

    def __openStuff(self, path):
        data=[]
        if os.path.exists(path):
            myF=open(path)
            raw_data=myF.readlines()
            for line in raw_data:
                data.append(line.strip())
        else:
            print '%s file not exist.' % path

        return data






