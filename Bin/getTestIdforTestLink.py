import os, sys
import Libs.CSVHandler as CSVHandler

default_path='../TestData'
desc={'Incident':'Test trigger rule -- %s',
      'LogDiscover':'Test using log to create %s device',
      'EventParsing':'Test parsing eventType %s'}
data_meta={'Incident':'incidentData',
           'LogDiscover':'logDiscoverData',
           'EventParsing':'eventParsingData'}

def getTestId(module):
    """This program is to create txt file for test ID.
    Usage: getTestIdforTestLink.py <module_name>"""
    module_path=default_path+'/'+module
    if not os.path.exists(module_path):
        print '%s is not exist. Exit.' % module_path
        sys.exit()
    data=[]
    if module=='EventParsing':
        folders=os.listdir(module_path)
        if '.svn' in folders:
            folders.remove('.svn')
        for f in folders:
            index_file=module_path+'/'+f+'/Index'
            data=CSVHandler.getDataFromFile(data_meta[module], index_file, None, None)
            myW=open(module+'.txt', 'w')
            for key in data.keys():
                holder=[]
                holder.append(key)
                holder.append(desc[module] % data[key].name)
                myW.write(','.join(holder)+'\n')
            myW.close()
    else:
        index_file=module_path+'/'+module[0].lower()+module[1:]+'Data.csv'
        data=CSVHandler.getDataFromFile(data_meta[module], index_file, None, None)
        myW=open(module+'.txt', 'w')
        for key in data.keys():
            holder=[]
            holder.append(key)
            holder.append(desc[module] % data[key].name)
            myW.write(','.join(holder)+'\n')
        myW.close()


if __name__=='__main__':
    if len(sys.argv)!=2:
        print getTestId.__doc__
        sys.exit()
    getTestId(sys.argv[1])
    print '\nTask is done.'

