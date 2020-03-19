"""This file contains information to create Summary Result template."""

summary_html_base="""
<html>
    <head>
        <title>Accelops Automation Test Report</title>
    </head>
    <body>
        <h1>Welcome to Accelops Automation Test</h1>
        <p>To view the most recent test results, please click the links to see the result:</p>
        <hr/>
        %s
    </body>
</html>
"""
content_html="""
        <h2>%s Test Result</h2>
        <hr/>
        %s
"""
date='<b>%s</b>'
content='<li><a href="http://%s/testresult/%s/report.html">%s</a></li>'
page='<p>%s</p>'
