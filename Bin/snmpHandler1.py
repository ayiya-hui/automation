#!/usr/bin/env python
#
# TRAP generator
#
# Copyright 1999-2006 by Ilya Etingof <ilya@glas.net>.
#
import string, sys, socket
from pysnmp_apps.cli import main, msgmod, secmod, target, pdu, mibview, base
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import ntforg, context
from pysnmp.proto.proxy import rfc2576
from pysnmp.proto import rfc1902
from pysnmp.proto.api import v1, v2c
from pysnmp import error

def getUsage():
    return "Usage: %s [OPTIONS] <MANAGER> <PARAMETERS>\n\
%s%s%s%s\
TRAP options:\n\
   -C<TRAPOPT>:   set various application specific behaviours:\n\
              i:  send INFORM-PDU, expect a response\n\
%s\
SNMPv1 TRAP management parameters:\n\
   enterprise-oid agent generic-trap specific-trap uptime <management-params>\n\
   where:\n\
              generic-trap:         coldStart|warmStart|linkDown|linkUp|authenticationFailure|egpNeighborLoss|enterpriseSpecific\n\
SNMPv2/SNMPv3 management parameters:\n\
   uptime trap-oid <management-params>\n\
%s" % (
        sys.argv[0],
        main.getUsage(),
        msgmod.getUsage(),
        secmod.getUsage(),
        mibview.getUsage(),
        target.getUsage(),
        pdu.getWriteUsage()
        )

# Construct c/l interpreter for this app

class Scanner(
    msgmod.MPScannerMixIn,
    secmod.SMScannerMixIn,
    mibview.MibViewScannerMixIn,
    target.TargetScannerMixIn,
    pdu.ReadPduScannerMixIn,
    main.MainScannerMixIn,
    base.ScannerTemplate
    ):
    def t_appopts(self, s):
        r' -C '
        self.rv.append(base.ConfigToken('appopts'))

    def t_genericTrap(self, s):
        r' coldStart|warmStart|linkDown|linkUp|authenticationFailure|egpNeighborLoss|enterpriseSpecific '
        self.rv.append(base.ConfigToken('genericTrap', s))

class Parser(
    msgmod.MPParserMixIn,
    secmod.SMParserMixIn,
    mibview.MibViewParserMixIn,
    target.TargetParserMixIn,
    pdu.WritePduParserMixIn,
    main.MainParserMixIn,
    base.ParserTemplate
    ):
    def p_trapParams(self, args):
        '''
        TrapV1Params ::= EnterpriseOid whitespace AgentName whitespace GenericTrap whitespace SpecificTrap whitespace Uptime whitespace VarBinds
        EnterpriseOid ::= string
        AgentName ::= string
        GenericTrap ::= genericTrap
        SpecificTrap ::= string
        Uptime ::= string

        TrapV2cParams ::= Uptime whitespace TrapOid whitespace VarBinds
        TrapOid ::= string
        '''

    def p_paramsSpec(self, args):
        '''
        Params ::= TrapV1Params
        Params ::= TrapV2cParams
        '''

    def p_appOptions(self, args):
        '''
        Option ::= ApplicationOption

        ApplicationOption ::= appopts whitespace string
        ApplicationOption ::= appopts string
        '''

class __Generator(base.GeneratorTemplate):
    def n_ApplicationOption(self, (snmpEngine, ctx), node):
        if len(node) > 2:
            opt = node[2].attr
        else:
            opt = node[1].attr
        for c in map(None, opt):
            if c == 'i':
                ctx['informMode'] = 1

    def n_EnterpriseOid(self, (snmpEngine, ctx), node):
        ctx['EnterpriseOid'] = node[0].attr

    def n_AgentName(self, (snmpEngine, ctx), node):
        try:
            ctx['AgentName'] = socket.gethostbyname(node[0].attr)
        except socket.error, why:
            raise error.PySnmpError(
                'Bad agent name %s: %s' % (node[0].attr, why)
                )

    def n_GenericTrap(self, (snmpEngine, ctx), node):
        ctx['GenericTrap'] = node[0].attr

    def n_SpecificTrap(self, (snmpEngine, ctx), node):
        ctx['SpecificTrap'] = node[0].attr

    def n_Uptime(self, (snmpEngine, ctx), node):
        ctx['Uptime'] = long(node[0].attr)

    def n_TrapV1Params_exit(self, (snmpEngine, ctx), node):
        v1Pdu = v1.TrapPDU()
        v1.apiTrapPDU.setDefaults(v1Pdu)
        if ctx.has_key('EnterpriseOid'):
            v1.apiTrapPDU.setEnterprise(v1Pdu, ctx['EnterpriseOid'])
        if ctx.has_key('AgentName'):
            v1.apiTrapPDU.setAgentAddr(v1Pdu, ctx['AgentName'])
        if ctx.has_key('GenericTrap'):
            v1.apiTrapPDU.setGenericTrap(v1Pdu, ctx['GenericTrap'])
        if ctx.has_key('SpecificTrap'):
            v1.apiTrapPDU.setSpecificTrap(v1Pdu, ctx['SpecificTrap'])
        if ctx.has_key('Uptime'):
            v1.apiTrapPDU.setTimeStamp(v1Pdu, ctx['Uptime'])
        v2cPdu = rfc2576.v1ToV2(v1Pdu)
        if not ctx.has_key('varBinds'):
            ctx['varBinds'] = []
        ctx['varBinds'] = v2c.apiPDU.getVarBinds(v2cPdu) + ctx['varBinds']

def generator((snmpEngine, ctx), ast):
    return __Generator().preorder((snmpEngine, ctx), ast)

snmpEngine = engine.SnmpEngine()

try:
    # Parse c/l into AST
    ast = Parser().parse(
        Scanner().tokenize(string.join(sys.argv[1:], ' '))
        )
    print(sys.argv[1:])
    print(ast)
    exit()

    ctx = {}

    # Apply configuration to SNMP entity
    main.generator((snmpEngine, ctx), ast)
    msgmod.generator((snmpEngine, ctx), ast)
    secmod.generator((snmpEngine, ctx), ast)
    mibview.generator((snmpEngine, ctx), ast)
    target.generatorTrap((snmpEngine, ctx), ast)
    pdu.writePduGenerator((snmpEngine, ctx), ast)
    generator((snmpEngine, ctx), ast)

except error.PySnmpError, why:
    sys.stderr.write('Error: %s\n%s' % (why, getUsage()))
    sys.exit(-1)


# Run SNMP engine

def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex,
          varBindTable, cbCtx):
    if errorIndication:
        sys.stderr.write('%s\n' % errorIndication)
        return
    if errorStatus:
        sys.stderr.write('%s\n' % errorStatus.prettyOut(errorStatus))
        return
    for varBindRow in varBindTable:
        colIdx = -1; inTableFlag = 0
        for oid, val in varBindRow:
            colIdx = colIdx + 1
            if val is None or not cbCtx['myHeadVars'][colIdx].isPrefixOf(oid):
                continue
            sys.stdout.write('%s\n' % cbCtx['mibViewProxy'].getPrettyOidVal(
                cbCtx['mibViewController'], oid, val
                ))
            inTableFlag = 1
        if not inTableFlag:
            return # stop on end-of-table
    return 1 # continue walking

snmpContext = context.SnmpContext(snmpEngine)

# Agent-side VACM setup
config.addContext(snmpEngine, '')
config.addTrapUser(snmpEngine, 1, ctx['securityName'],
                   'noAuthNoPriv', (1,3,6)) # v1
config.addTrapUser(snmpEngine, 2, ctx['securityName'],
                   'noAuthNoPriv', (1,3,6)) # v2c
config.addTrapUser(snmpEngine, 3, ctx['securityName'],
                   'authPriv', (1,3,6)) # v3

ctx['notificationName'] = 'myNotifyName'
config.addNotificationTarget(
    snmpEngine, ctx['notificationName'], ctx['paramsName'],
    ctx['transportTag'], 'trap'
    )

ntforg.NotificationOriginator(snmpContext).sendNotification(
    snmpEngine, ctx['notificationName'], ('SNMPv2-MIB', ctx['GenericTrap']),
    ctx['varBinds'], cbFun, ctx
    )

try:
    snmpEngine.transportDispatcher.runDispatcher()
except error.PySnmpError, why:
    sys.stderr.write('Error: %s\n' % why)
    sys.exit(-1)
