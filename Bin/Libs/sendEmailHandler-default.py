import smtplib
from email.MIMEText import MIMEText
from email.mime.multipart import MIMEMultipart
from AutoTestUtil.testPrepare import getTestConfig

SUBJECT='%s-AccelOps VA automation result'
EMAIL_USER='notify'
EMAIL_PWD='(jWohE68N'
#MAIL_GATEWAY='smtpx16.msoutlookonline.net'
MAIL_GATEWAY='outlook.office365.com'
DEFAULT_PORT=25
#DEFAULT_RECIPIENTS= ['QA.US']
#DEFAULT_RECIPIENTS=['Eng.USA','Eng.China']
#DEFAULT_RECIPIENTS=['hui.huang','Zhensong.Ye']
#DEFAULT_RECIPIENTS=['hui.huang']

#DEFAULT_RECIPIENTS=['chunying.yang']
DEFAULT_RECIPIENTS=['chunying.yang']
#DEFAULT_RECIPIENTS=['siva.abbannagari']

DEFAULT_DOMAIN='accelops.com'


class sendEmailHandler:
    """This class will handle sendmail utility to send out notification mail for autobuilder automation.
    It will send by notify@accelops.com mail account and to ENG mailing list (USA and China)."""
    def __init__(self, host=MAIL_GATEWAY, port=DEFAULT_PORT,user=EMAIL_USER, pwd=EMAIL_PWD, recipt=DEFAULT_RECIPIENTS, domain=DEFAULT_DOMAIN):
        self.host=host
        self.port=port
        self.user=user
        self.pwd=pwd
        self.recipt=recipt
        self.domain=domain
        self.smtp=smtplib.SMTP(self.host, self.port)

    def _getSender(self):
        return self.user+'@'+self.domain

    def _getRecepts(self):
        names=[]
        for name in self.recipt:
            names.append(name+'@'+self.domain)

      #  return ' '.join(names)
        return names

    def sendEmail(self, msg, test_name):
        """This method will take the message and send the email."""
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.ehlo()
        sender=self._getSender()
        recipts=self._getRecepts()
        self.smtp.login(sender, self.pwd)

        myMail=MIMEMultipart('alternative')
        myMail['Subject']=SUBJECT % test_name
        myMail['From']=sender
        myMail['To']=";".join(recipts)
        html=MIMEText(msg,'html')
        myMail.attach(html)
        self.smtp.sendmail(sender, recipts, myMail.as_string())
        self.smtp.quit()


if __name__ == "__main__":
    handler = sendEmailHandler()
    handler.sendEmail("test")
