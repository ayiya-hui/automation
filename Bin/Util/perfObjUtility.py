import Libs.restApiDataHandler as restApiHandler

perf_object_list=['sys_uptime_id','sys_cpu_id', 'sys_mem_id', 'sys_stat_id', 'sys_processes_id', 'sys_disk_id']

def getPerfObj(appServer):
    rawPerfObj=restApiHandler.restApiDataHandler(appServer).getData('perfObject')
    perfMap={}
    for perfId in rawPerfObj:
        pType=rawPerfObj[perfId].type
        typeName=pType.name.lower()+'_id'
        if typeName in perf_object_list:
            perfMap[typeName]=perfId

    return perfMap

