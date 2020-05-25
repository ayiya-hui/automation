# -*- coding:utf-8 -*
#@Time      : 4/15/2020 
#@Author   : Hui Huang

import paramiko
from xml.dom.minidom import parseString
import csv

def checkNewLogDiscoverCase(appserver):
    csvlist =[]
    with open('/root/logDiscoverData.csv', 'r') as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            csvlist.append(line)
    parsers = ['AIDEParser.xml','CyberoamParser.xml','InfoBloxAppParser.xml','RadwareParser.xml','AirTightSpectraGuardParser.xml','CylanceProtectParser.xml','InfoBloxAuditParser.xml','Rapid7InsightVMVulnParser.xml','AirWatchParser.xml','CyphortParser.xml','InfoBloxTrapParser.xml','RaxNexposeReportParser.xml','AIXParser.xml','CyxteraParser.xml','IPswitchWS_FTPParser.xml','RaxRapid7CsvParser.xml','AlcatelAAAParser.xml','DamballaParser.xml','IronportMailParser.xml','RaxSecureWorksScanParser.xml','AlcatelOmniSwitchesParser.xml','IronportWebParser.xml','ReconnextLogParser.xml','AlertLogicParser.xml','DataPowerParser.xml','ISAServerParser.xml','RiverbedSteelheadParser.xml','AOWUA_DHCPParser.xml','DellEqualLogicParser.xml','IsilonParser.xml','RSAAuthenticationServerParser.xml','AOWUA_DNSParser.xml','DellForce10Parser.xml','JBossAccessLogParser.xml','RSASParser.xml','AOWUA_IISParser.xml','DellHwChassisTrapParser.xml','JBossLogParser.xml','RuckusParser.xml','AOWUA_WinParser.xml','DellHwStorageTrapParser.xml','JEEAppServerParser.xml','SalesforceParser.xml','ApacheViaSnareParser.xml','DellNSeriesParser.xml','JuniperDDoSParser.xml','SecurityOnionBroParser.xml','APCParser.xml','DellPowerConnectParser.xml','JuniperSteelBeltAAAParser.xml','SendmailParser.xml','ArborSpectrumParser.xml','DigitalGuardianDLPParser.xml','JunipNSM-IDP.xml','SendMailPopImapParser.xml','ArubaOSSyslogParser.xml','DynaTraceParser.xml','JunipNSM-SSG.xml','SentinelOneParser.xml','ArubaPolicyManager2Parser.xml','EDirectoryCEFParser.xml','JunipSSGFirewallLog.xml','SnortParser.xml','ArubaPolicyManagerParser.xml','EmcParser.xml','JunipSSLVPN.xml','SolarisLogParser.xml','ArubaWLANParser.xml','EpicSecuritySIEMParser.xml','JunOS2Parser.xml','SonicWallAventailNetWorkAndWebProxyParser.xml','AS400CEFParser.xml','ESETNode32Parser.xml','JunOSParser.xml','SonicWallAventailSyslogParser.xml','AstaroSecureGwParser.xml','ESETParser.xml','KasperskyParser.xml','SonicWallAventailWorkPlaceParser.xml','AvayaCMParser.xml','ExtremeSwitchParser.xml','LantronixSLCParser.xml','SonicwallFirewallParser.xml','AWSELBParser.xml','F5AFMParser.xml','LastlineParser.xml','SophosCentralParser.xml','AwsFlowLogParser.xml','F5ASMCEFParser.xml','LinuxAuditdParser.xml','SophosParser.xml','AwsKinesisParser.xml','F5Big-IP-LTMParser.xml','LinuxDHCPParser.xml','SophosUTMParser.xml','F5BigIP-OSTrapParser.xml','LinuxInotifyParser.xml','SophosWebFilterParser.xml','AzureEventHubParser.xml','F5Parser.xml','MalwarebytesParser.xml','SophosXGFirewallParser.xml','BarracudaFirewallParser.xml','F5WebAcceleratorParser.xml','McAfeeAVParser.xml','Sourcefire2Parser.xml','BarracudaWebFilterParser.xml','FalconDataRepParser.xml','McAfeeFwSyslogParser.xml','Sourcefire3Parser.xml','BindDNSParser.xml','FalconStreamingParser.xml','McAfeeIPSSyslogParser.xml','SourcefireParser.xml','Bit9Parser.xml','FimParser.xml','McAfeeStonesoftParser.xml','SquidParser.xml','BitdefenderGravityZoneParser.xml','FireAMPCloudParser.xml','McAfeeVormetricParser.xml','SymantecAVParser.xml','BlueCoatAuthParser.xml','FireEyeETPParser.xml','McAfeeVulnMgrParser.xml','SymantecDLPParser.xml','BlueCoatParser.xml','FireEyeJsonParser.xml','McAfeeWebGatewayParser.xml','SymantecSAPCEFParser.xml','BluecoatWebProxyParser.xml','FireEyeParser.xml','McAfeeXmlParser.xml','SymantecSAPParser.xml','BoxParser.xml','FireEyeTrapParser.xml','MicrosoftAzureATPParser.xml','SymantecWebIsolationParser.xml','BrocadeSanSwitchParser.xml','FireMonParser.xml','MicrosoftAzureAuditParser.xml','SyslogNGParser.xml','CarbonBlackCEFParser.xml','FlowTraqParser.xml','MicrosoftCloudAppSecurityCEFParser.xml','TaniumConnectParser.xml','CarbonBlackParser.xml','ForcepointESGCEFParser.xml','MicrosoftDHCPTrapParser.xml','TenableVulnParser.xml','CheckpointCEFParser.xml','ForeScoutCEFParser.xml','MicrosoftExchangeTrackingLogParser.xml','TipPointIPSParser.xml','CheckpointGAIAParser.xml','ForeScoutCounterACTParser.xml','MicrosoftIASODBCParser.xml','TipPointNMSParser.xml','CheckpointParser.xml','FortiADCParser.xml','MicrosoftIASParser.xml','TipPointSysAuditParser.xml','CimTrakParser.xml','FortiAuthenticatorParser.xml','MicrosoftNPSParser.xml','TrendMicroApexCentralParser.xml','CiscoACEParser.xml','FortiClientParser.xml','MicrosoftPPTPParser.xml','TrendMicroDeepDiscoveryParser.xml','CiscoACIParser.xml','FortiDDoSParser.xml','MicrosoftUAGParser.xml','TrendMicroDeepSecurityParser.xml','CiscoACSParserPlus.xml','FortiDeceptorParser.xml','MikroTikFirewallParser.xml','TrendMicroIDFParser.xml','CiscoACSParser.xml','FortiEDRParser.xml','MobileIronParser.xml','TrendMicroInterscanWebSecurityParser.xml','CiscoAMPParser.xml']
    nparsers = []


    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('10.30.2.113', 22, 'root', 'ProspectHills')
    f = open('/root/1.txt', 'w')
    for parser in parsers:
        cmd = 'cat /opt/phoenix/config/xml/{}'.format(parser)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode()
        #print(reg.findall(out))
        domTree = parseString(out)
        vendor = domTree.getElementsByTagName('Vendor')[0].childNodes[0].data
        model = domTree.getElementsByTagName('Model')[0].childNodes[0].data
        event = domTree.getElementsByTagName('testEvent')[0].childNodes[0].data
        Parserdetail = []
        flag = 0
        if (vendor == 'Alert Logic' and model =='IPS') or (vendor == 'Box.com' and model =='Box') or \
                (vendor == 'Cisco' and model == 'FireAMP Cloud') or (vendor == "CloudPassage" and model == "Halo") or \
                (vendor == "CrowdStrike" and model == "Falcon") or (vendor == "GitHub.com" and model == "GitHub") or \
                (vendor == "GitLab" and model == "GitLab") or (vendor == "Google" and model == "Google Apps") or \
            (vendor == "Microsoft" and model == "Office365") or (vendor == "Microsoft" and model == "Windows Defender ATP") or \
            (vendor == "Qualys" and model == "QualysGuard Scanner") or (vendor == "Salesforce" and model == "Salesforce Audit") or \
            (vendor == "Sophos" and model == "Central") or (vendor == "Tenable" and model == "Tenable.io"):
            pass
        elif ('Generic' not in vendor) and ('Generic' not in model):
            for line in csvlist:
                if line[3] == vendor and line[2] == model:
                    flag = 1
            if flag ==0:
                nparser = parser.split('Parser.')[0]
                Parserdetail.append(nparser)
                Parserdetail.append('')
                Parserdetail.append(model)
                Parserdetail.append(vendor)
                with open('/root/parser/'+nparser+'.dat','a+') as ff:
                    ff.write("[eventMsg]\n")
                    ff.write(event)
                    ff.close()
                #Parserdetail["event"] = event
                print('Found new logdiscover cases, and save to /root/1.txt')
                f.write(str(Parserdetail)+'\n')
    f.close()
    ssh.close()

if __name__=='__main__':
    import sys
    if len(sys.argv)!=2:
        print checkNewParsers.__doc__
        sys.exit()
    checkNewParsers(sys.argv[1])
    print 'Task is done.'
