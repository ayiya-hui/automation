import getCmdsSelenium
import AOBrowserCore
import cssify
from string import Template
import time, re
import urlparse

step='<step id="$id" name="$name" result="$status" timeMs="$time"/>'
final='<seleniumScriptResult result="$result" $special><steps>$steps</steps></seleniumScriptResult>'
special={'Pass':'timeMs="$time"', 'Fail':'errMsg="$errMsg"'}

class AOBrowser:
    def __init__(self, debug=False, timeout=False):
        self.debug=debug
        self.AO=AOBrowserCore.AOBrowserCore(display=True, debug=self.debug, wait_timeout=timeout)

    def replay(self, cmdList, output):
        i=1
        steps=[]
        finalStatus='Pass'
        finalError=''
        myTemp=Template(step)
        sTime=time.time()
        previous_execution_time=sTime
        try:
            for cmd in cmdList:
                myMap={}
                myMap['id']=str(i)
                myMap['name']=cmd.msg
                status, errMsg=self.excuteCmd(cmd)
                myMap['status']=status
                if status=='Fail':
                    myMap['errorMsg']=errMsg
                    finalStatus=status
                    finalError=errMsg+' at Step '+str(i)
                execution_time=time.time()
                diff=round(execution_time-previous_execution_time, 2)
                myMap['time']=diff
                previous_execution_time=execution_time
                i+=1
                steps.append(myTemp.substitute(myMap))
                if status=='Fail':
                    break
        except Exception, e:
            finalStatus='Fail'
            finalError='AOBrowser has %s: %s' % (e.__class__.__name__, e)
        fTime=time.time()
        mySpecial=Template(special[finalStatus])
        specialMap={}
        if finalStatus=='Pass':
            specialMap['time']=round(fTime-sTime, 2)
        else:
            specialMap['errMsg']=finalError
        specialStr=mySpecial.substitute(specialMap)
        myFinalTemp=Template(final)
        myFinal={'result':finalStatus, 'special':specialStr, 'steps':''.join(steps)}
        finalStr=myFinalTemp.substitute(myFinal)
        myW=open(output, 'w')
        myW.write(finalStr)
        myW.close()
        finalResult=''
        if finalStatus=='Pass':
            finalResult=finalStatus
        else:
            finalResult+=': '+finalError

        return finalResult

    def assertItem(self, cmd):
        if cmd.cmd_name=='waitForText':
            cmd.cmd_name='assertText'
            cmd.assert_opt='positive'
        token_value=''
        condition=''
        status=''
        errMsg=''
        if 'Not' in cmd.cmd_name:
            token_value=cmd.cmd_name.split('assertNot')[-1]
        else:
            token_value=cmd.cmd_name.split('assert')[-1]
        if token_value in ['Text', 'TextPresent', 'Table']:
            if cmd.target[0]=='*' and cmd.target[-1]=='*':
                value=cmd.target[1:-1]
            else:
                value=cmd.target
            ret, res=self.AO.wait_for_text(value)
            if ret:
                condition=True
            else:
                condition=False
        elif token_value=='Title':
            if cmd.params['objValue']==self.AO.main_frame.title():
                condition=True
            else:
                condition=False
        elif token_value=='ElementPresent':
            selectors, my_op, my_val=self.getCSSSelector(cmd, name='')
            if len(selectors):
                for s in selectors:
                    ret, element=self.AO.wait_for_selector(s, my_op, my_val)
                    if ret:
                        condition=True
                    else:
                        conddtion=False
        else:
            status='Fail'
            errMsg='Assert%s is not supported' % token_value
        opt_value=cmd.assert_opt
        if opt_value=='positive':
            if condition:
                status='Pass'
            else:
                status='Fail'
                errMsg='assert%s %s was not matched.' %(token_value, cmd.params['objValue'])
        else:
            if condition:
                status='Fail'
                errMsg='assert%S %s was matched.' %(token_value, cmd.params['objValue'])
            else:
                status='Pass'

        return status, errMsg

    def excuteCmd(self, cmd):
        if self.debug:
            print 'start on:', cmd.cmd_name, cmd.params
        status=''
        errMsg=''
        tag_name=''
        if cmd.cmd_name=='selectFrame':
            tag_name='iframe'
        if cmd.cmd_type=='open':
            url=cmd.params['objValue']
            page, extra=self.AO.open(url)
            if page is not None and page.http_status==200:
                status='Pass'
            else:
                status='Fail'
                errMsg='Cannot open page %s' % url
        elif cmd.cmd_type=='wait':
            status='Pass'
            wait_time=float(int(cmd.target)/100000)
            time.sleep(wait_time)
        elif cmd.cmd_type=='assert':
            status, errMsg=self.assertItem(cmd)
        elif cmd.cmd_type=='click' and cmd.cmd_name=='selectFrame':
            iframes=self.AO.handleFrames(i=True)
            if not iframes.count==0:
                for iframe in iframes:
                    print iframe.attribute('id')
                    if cmd.params is not None:
                        id=cmd.params['objValue']
                url=str(iframes[0].attribute('src'))
                final_url=urlparse.urljoin(self.AO.base_url, url)
                page, extra=self.AO.open(final_url)
                if page is not None and page.http_status==200:
                    status='Pass'
                else:
                    status='Fail'
                    errMsg='Cannot open iframe'
        else:
            selectors, my_op, my_val=self.getCSSSelector(cmd, name=tag_name)
            if len(selectors):
                for s in selectors:
                    ret, element=self.AO.wait_for_selector(s, my_op, my_val)
                    if ret:
                        ret1=''
                        msg=''
                        if cmd.cmd_type=='input':
                            ret1, res=self.AO.set_field_value(s, cmd.target)
                            msg='Set file value'
                        elif cmd.cmd_type=='click':
                            ret1, msg=self.actionClick(s, my_op, my_val)
                        if ret1:
                            status='Pass'
                        else:
                            status='Fail'
                            errMsg='%s did not return true.' % msg
                    else:
                        #check for frame
                        frames=self.AO.handleFrames()
                        if not frames.count()==0:
                            for frame in frames:
                                url=str(frame.attribute('src'))
                                final_url=urlparse.urljoin(self.base_url, url)
                                page, extra=self.AO.open(final_url)
                                if page is not None and page.http_status==200:
                                    ret, element=self.AO.wait_for_selector(s, my_op, my_val)
                                    if ret:
                                        ret1, msg=self.actionClick(s, my_op, my_val)
                                        if ret1:
                                            status='Pass'
                                        else:
                                            status='Fail'
                                            errMsg='Click %s did not return true' % msg
                                        break
                            if not ret:
                                status='Fail'
                                errMsg='Element %s is not in frames' % my_val
                        else:
                            status='Fail'
                            errMsg='Element %s does not exist' % cmd.params['objValue']
            else:
                status='Fail'
                errMsg='Does not have css selector'

        return status, errMsg

    def actionClick(self, s, my_op, my_val):
        ret=''
        msg=''
        if hasattr(self.AO, 'a_link') and self.AO.a_link:
            ret, res=self.AO.click(self.AO.a_link, '', '')
            msg='Click link %s' % self.AO.a_link
        else:
            ret, res=self.AO.click(s, my_op, my_val)
            msg='Click link %s' % my_val
            if not ret:
                al_url=''
                if hasattr(self.AO, 'nofollow') and self.AO.nofollow:
                    al_url=self.AO.nofollow
                elif hasattr(self.AO, 'alter_url') and self.AO.alter_url:
                    al_url=self.AO.alter_url
                if al_url:
                    page, extra=self.AO.open(al_url)
                    msg='click alternate link %s' % al_url
                    if page is not None and page.http_status==200:
                        ret=True
            self.AO.nofollow_link=''
            self.AO.nofollow=''
            self.AO.alter_url=''
        if ret:
            pages, res=self.AO.wait_for_page_loaded()

        return ret, msg

    def exit(self):
        del self.AO

    def getCSSSelector(self, cmd, name=''):
        selectors=[]
        op=''
        value=''
        if cmd.params is not None:
            obj=cmd.params['obj']
            if obj=='id':
                if name:
                    selectors.append('%s#%s' % (name, cmd.params['objValue']))
                else:
                    selectors.append('#%s' % cmd.params['objValue'])
            elif obj=='name':
                if name:
                    selectors.append('%s[name="%s"]' % (name, cmd.params['objValue']))
                else:
                    selectors.append('[name="%s"]' % cmd.params['objValue'])
            elif obj=='identifier':
                if name:
                    selectors.append('%s#%s' % (name, cmd.params['objValue']))
                    selectors.append('%s[name="%s"]' % (name, cmd.params['objValue']))
                else:
                    selectors.append('#%s' % cmd.params['objValue'])
                    selectors.append('[name="%s"]' % cmd.params['objValue'])
            elif obj=='link':
                selectors.append('a')
                op='text'
                value=getCmdsSelenium.revertEscape(cmd.params['objValue'])
            elif obj=='css':
                selectors.append(cmd.params['objValue'])
            elif obj=='xpath':
                if cmd.params['objValue'].startswith('(//a[contains(text(),') or cmd.params['objValue'].startswith('//a[contains(text(),'):
                    sel, op, value=cssify.cssifyContainText(cmd.params['objValue'])
                else:
                    sel=cssify.cssify(cmd.params['objValue'])
                selectors.append(sel)
            else:
                if self.debug:
                    print 'Need to handle %s' % cmd.params['obj']

        return selectors, op, value

