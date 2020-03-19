import test
from ConfigConstants.TestConstant import default_config_file_path

total=8
d=8
name='incidentBatch%i.xml'
for i in range(total):
    file=default_config_file_path+(name % (i+1))
    print file
    test.autoTest(file)

print 'All tasks are done.'
