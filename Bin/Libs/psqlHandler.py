import os
import ConfigConstants.TestConstant as TestConstant

class psqlHandler:
    """This class will handle psql command line utility. The remote PostGress database
    needs to turn off interactive authentication."""
    def __init__(self, host, port=False, user=False, password=False, database=False):
        option={}
        option['-h']=host
        if port and host!=TestConstant.sql_default_port:
            option['-p']=port
        if user:
            option['-U']=user
        else:
            option['-U']=TestConstant.sql_default_user
        if database:
            option['-d']=database
        else:
            option['-d']=TestConstant.sql_default_database_name
        option['-c']='"%s"'
        self.cmd='psql'
        for opt in option.keys():
            self.cmd+=' '+opt+' '+option[opt]

    def execute(self, cmd, pick=True):
        """This method will excute a SQL command and return the data."""
        myCmd=self.cmd % cmd
        text=os.popen(myCmd).read()
        data=[]
        if text:
            if pick:
                heads, garbage, contents=text.split('\n', 2)
                contentList=contents.strip().split('\n')[0:-1]
                for content in contentList:
                    row=content.strip().split('|')
                    newRow=[]
                    for item in row:
                        newRow.append(item.strip())
                    data.append(newRow)
            else:
                print text
        else:
            print 'SQL query return no data'
            exit()

        return data



