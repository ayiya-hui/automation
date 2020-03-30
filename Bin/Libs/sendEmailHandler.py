import smtplib
from email.MIMEText import MIMEText
from email.mime.multipart import MIMEMultipart
import pdb


class sendEmailHandler:
    """This class will handle sendmail utility to send out notification mail for autobuilder automation.
    It will send by notify@accelops.com mail account and to ENG mailing list (USA and China)."""
    def __init__(self, recipt):
        #self.host='outlook.office365.com'
        self.host='smtp.aliyun.com'
        self.port=25
        #self.user='notify'
        #self.pwd='(jWohE68N'
	self.user='accelopsautomation'
        self.pwd='ProspectHills!'
        self.recipt=filter(None,[i.strip() for i in recipt])
        self.domaind='fortinet.com'
		#self.domaind='accelops.com'
        self.domains='aliyun.com'
        #pdb.set_trace()
        self.smtp=smtplib.SMTP(self.host, self.port)

    def _getSender(self):
        return self.user+'@'+self.domains

    def _getRecepts(self):
        names=[]
        for name in self.recipt:
            names.append(name+'@'+self.domaind)

      #  return ' '.join(names)
        return names

    def sendEmail(self, msg, test_name, run_version):
        """This method will take the message and send the email."""
        #self.smtp.set_debuglevel(True)
        #self.smtp.ehlo()
        #self.smtp.starttls()
        self.smtp.ehlo()
        sender=self._getSender()
        recipts=self._getRecepts()
        self.smtp.login(sender, self.pwd)

        myMail=MIMEMultipart('alternative')
        myMail['Subject']='%s-AccelOps VA automation result(%s)' % (test_name,run_version)
        myMail['From']=sender
        myMail['To']=";".join(recipts)
        html=MIMEText(msg,'html')
        myMail.attach(html)
        self.smtp.sendmail(sender, recipts, myMail.as_string())
        self.smtp.quit()


if __name__ == "__main__":
    handler = sendEmailHandler(["hhuang",])
    handler.sendEmail("test", "aa", "1.1")
