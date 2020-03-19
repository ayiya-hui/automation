ruleTestEvents="""
<testEvents id="$rule_id">
    $events
</testEvents>"""

ruleTestEvent="""
<testEvent reportIp="$report_ip" pause="$pause" sequence="$number"><![CDATA[$raw_event]]></testEvent>"""

html_content="""
<html>
    <head>
        <script src="sorttable.js" type="text/javascript"></script>
        <style type="text/css">
            #test { padding: 5px;
                    border-collapse: collapse;
                    border: 1px solid #000000;
                    width: 50%;
                    }
            #test td { border: 1px solid #000000;
                       padding: 3px;
                       font-size: .9em;
                    }
            #test th { border: 1px solid #000000;
                       background-color: #CCFFCC;
                    }
            #netflow { padding: 5px;
                    border-collapse: collapse;
                    border: 1px solid #000000;
                    width: 50%;
                    }
            #netflow td { border: 1px solid #000000;
                       padding: 3px;
                       font-size: .9em;
                    }
            #netflow th { border: 1px solid #000000;
                       background-color: #00FFCC;
                    }
            #nosupport { padding: 5px;
                    border-collapse: collapse;
                    border: 1px solid #000000;
                    width: 50%;
                    }
            #nosupport td { border: 1px solid #000000;
                       padding: 3px;
                       font-size: .9em;
                    }
            #nosupport th { border: 1px solid #000000;
                       background-color: #00FFCC;
                    }
        </style>
        <title>Accelops Automation Test Rule Result</title>
    </head>
    <body>
        <h2>Total $test_count rules tested.</h2>
        <table id="test" class="sortable">
            <tr>
                <th>Rule Name</th>
                <th>Rule ID</th>
                <th>Result</th>
                <th>Reason</th>
            </tr>
            $test
        </table>
        <hr/>
        <h2>Total $netflow_count rules not tested due to lack of support.</h2>
        <table id="netflow" class="sortable">
            <tr>
                <th>Rule Name</th>
                <th>Rule ID</th>
            </tr>
            $netflow
        </table>
        <h2>Total $nosupport_count rules not tested due to not adding in automation.</h2>
        <table id="nosupport" class="sortable">
            <tr>
                <th>Rule Name</th>
                <th>Rule ID</th>
            </tr>
            $nosupport
    </body>
</html>
"""

table_body="""
        <tbody>
            $tableBody
        </tbody>
"""

test_table_row="""
        <tr>
            <td>$name</td>
            <td>$id</td>
            <td>$result</td>
            <td>$reason</td>
        </tr>
"""

other_table_row="""
        <tr>
            <td>$name</td>
            <td>$id</td>
        </tr>
"""
