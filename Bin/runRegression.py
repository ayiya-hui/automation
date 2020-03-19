import test
from ConfigConstants.TestConstant import default_config_file_path

names=['logDiscover', 'eventParsingConfig','DailyIncident']
for name in names:
    file=default_config_file_path+name+'.xml'
    print file
    test.autoTest(file)

print 'All tasks are done.'
