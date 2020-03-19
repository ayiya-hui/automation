import Libs.expressionReader as expressionReader

host='192.168.20.116'
param='COUNT(*) >= 2'
expressionReader.expressionReader(param, host, option='group')