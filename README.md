# 1. How to get the tools ready?

## (1) svn checkout
check out the codes with the following instruction:

    svn co https://svn.accelops.net/svn/AutoAccelops

## (2) what python packages are needed?
The required packages are httplib2, pexpect and IPy


# 2. How to run a regression test?


## (1) complete regression
The compete regression contains three files: EventParsing-weisun.xml
Logdiscover-weisun.xml and Incident-weisun.xml.
we should enter the objective folder with the permission of root

    cd /AutoAccelops/Bin

Then, we run the test.py with the following command with your own file. For example,
EventParsing-weisun.xml is created by weisun himself, and the following commands can be executed by weisun himself.

    root> python test.py EventParsing-weisun
    root> python test.py Incident-weisun
    root> python test.py Logdiscover-weisun
We will receive the details of the execution of these commands
EventParsing-weisun.xml is the file that you want to conduct

## (2) event parsing only
We can also execute the event parsing only in the following.

    cd /AutoAccelops/Bin
    python test.py EventParsing-weisun
Then, we can receive the results of executing this event parsing with email immediately.


## (3) test on which machine
There is a file to setup the environment of running the regression test.
Before runing the regression test, we should assure which machine we want to test.
Therefore,

    cd AutoAccelops/ConfigFiles
    vi EventParsing-weisun.xml // you can create your own file.
    <allInOne>10.1.20.31</allInOne> // IP is your AO.
    <taskFiles>ALL</taskFiles>  // All change to the test parser name.
## (4) send email to someone
we can get the result of runing the regression test.

    cd AutoAccelops/Bin/Libs/
    vi sendEmailHandler.py
    DEFAULT_RECIPIENTS=['wei.sun'] //change to your own email address.



# 3. How to add a case?

We take the ISAServerParser as an example.

## (1) creating a text file and then saving the event logs to it e.g. isaweb.txt
where isaweb.txt can contain the two types of event logs as follows:

    Mar 30 17:46:56 192.168.20.3 ISAWebLog 0 10.1.2.10      anonymous       -       Y       2011-05-30      09:46:29        w3proxy SH-WIN03-QA     -       125.39.149.44   125.39.149.44   80      1       142     2251    http    TCP     POST    http://125.39.149.44/   -       -       12202   0x0     Default rule    Req ID: 15a18b1d; Compression: client=No, server=No, compress rate=0% decompress rate=0%        Local Host      External        0x200   Denied  2011-05-30      09:46:29        -

    <13>Mar  6 20:56:03 192.168.23.5  ISAWebLog     0       192.168.69.9    anonymous       Mozilla/5.0 (Windows; U; Windows NT 5.2; en-GB; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12      Y       2011-03-05      21:33:55        w3proxy ISA     -       2.2.2.2 2.2.2.2 80      156     636     634     http    TCP     GET     http://2.2.2.2/rss/newsonline_uk_edition/front_page/rss.xml     text/html; charset=iso-8859-1   Inet    301     0x41200100      Local Machine   Req ID: 07c10445; Compression: client=No, server=No, compress rate=0% decompress rate=0%        Local Host      External        0x400   Allowed 2011-03-05 21:33:55     -

## (2) running the command to send the event logs to your AO as well as add new cases to the pointed directory

    python addEventParsingCase.py 10.1.20.31 -f isaweb.txt -m ISAServer

ISAServer is the directory name. You can see all the directories under

    AutoAccelops/TestData/EventParsing

## (3) results of adding cases
we can see two files, which are added into the folder of ISAServer such as ISA-Proxy-202-Accepted.dat and ISA-Proxy-301-Moved-Permanently.dat
Then, we check whether the data in the these two files are the same with what we send in the step(2).
If not, we should clean the history of the sended event logs, or decrease the duration our program gets the event logs.
For example, we change

     params['minute']='60' to params['minute']='1'

in the file of queryHandler.py

# 4. How to include the result to httpd?
We should configure httpd setting on our own machine to see the regression test result.

    cd /var/www/html

Now we are in the directory where the testresult is located.

    ln -s /AutoAccelops/Results/ testresult

Now we set up a symbolic link to the target in the testresult directory and now the link in the test report email as below can direct us to see the test result details.

    http link: http://10.1.20.31/testresult/EventParsing-2016-06-24-162248-10.1.20.31/report.html

# 5. How to successfully add cases with agelong phRecvTime?
For some parsers, the event Receive Time maybe manually assigned. For example, for SalesforceParser:

    <setEventAttribute attr="phRecvTime">$deviceTime</setEventAttribute>
	
In this case, if the assigned phRecvTime is too long ago, the historical research may fail to detect this event, which will lead to a case-adding failure like:

    1.txt   [Salesforce_Activity_Perf]:[activityType]=API,[activityName]=get_user_info,[srcIpAddr]=23.23.13.166,[user]=huiping.hp@gmail.com,[deviceTime]=1458112097,[isSuccess]=false,[runTime]=31,[cpuTime]=9,[dbTime]=19434051,[infoURL]=Api

    root> python addEventParsingCase.py 10.1.20.31 -f 1.txt -m Salesforce
	No case returned
    Not add new cases.
	
In this case, we need to manually modified the deviceTime in the rawEventMsg by assigning a recent time to it as following:

    root> python
	>>> import time
    >>> time.time()
    1468462527.40705
	
	1.txt
	[deviceTime]=1458112097 -> [deviceTime]=1468462407
	(we deduct 120s from the present time to ensure the success of historical research)
	
Then we can rerun the addEventParsingCase.py and we can find the new dat is added successfully like:

    root> python addEventParsingCase.py 10.1.20.31 -f 1.txt -m Salesforce
    New case eventType: Salesforce_Activity_Perf
    add new cases.

