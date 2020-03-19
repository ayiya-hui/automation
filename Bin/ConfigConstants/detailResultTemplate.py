"""This file contains Detail Result Templates."""

report_html="""
<html>
    <head>
        <script src="sorttable.js" type="text/javascript"></script>
        <style type="text/css">
            #main { padding: 5px;
                    border-collapse: collapse;
                    border: 1px solid #000000;
                    width: 100%;
                    }
            #main td { border: 1px solid #000000;
                       padding: 3px;
                       font-size: .9em;
                    }
            #main th { border: 1px solid #000000;
                       background-color: #CCFFCC;
                    }
            #no_return { padding: 5px;
                    border-collapse: collapse;
                    border: 1px solid #000000;
                    width: 100%;
                    }
            #no_return td { border: 1px solid #000000;
                       padding: 3px;
                       font-size: .9em;
                    }
            #no_return th { border: 1px solid #000000;
                       background-color: #00FFCC;
                    }
            #fail { padding: 5px;
                    border-collapse: collapse;
                    border: 1px solid #000000;
                    width: 100%;
                    }
            #fail td { border: 1px solid #000000;
                       padding: 3px;
                       font-size: .9em;
                    }
            #fail th { border: 1px solid #000000;
                       background-color: #00FFCC;
                    }
            #no_implement { padding: 5px;
                    border-collapse: collapse;
                    border: 1px solid #000000;
                    width: 100%;
                    }
            #no_implement td { border: 1px solid #000000;
                       padding: 3px;
                       font-size: .9em;
                    }
            #no_implement th { border: 1px solid #000000;
                       background-color: #00FFCC;
                    }
        </style>
        <title>Accelops Automation Test Report</title>
    </head>
    <body>
        <h1>Test Report</h1>
        <hr/><b>Test Type: $testType</b>
        <hr/>
        <b>Test Running Time: $runTime, Test Target Build Version: $runVersion</b>
        <hr/>
        <p>Please click on the title to sort the result.</p>
        <table id="main" class="sortable">
            <thead>
            <tr>
                <th>Module</th>
                <th>Suite</th>
                <th>Total Test</th>
                <th>Test Passed</th>
                <th>No Return Data</th>
                <th>Test Failed</th>
                <th>Detail Results</th>
            </tr>
            $mainTable
        </table>
        $optionTable
    </body>
</html>
"""

no_return_table="""
        <h2>Testcases have No Return:</h2>
        <table id="no_return" class="sortable">
            <tr>
                <th>Test Case Name</th>
                <th>Test Module Name</th>
                <th>Test Suite Name</th>
                <th>testRule Result</th>
                <th>Reasons</th>
            </tr>
            $NoReturn
        </table>
"""

fail_table="""
        <h2>Testcases have return but some parameters are not correct:</h2>
        <table id="fail" class="sortable">
            <tr>
                <th>Test Case Name</th>
                <th>Test Module Name</th>
                <th>Test Suite Name</th>
                <th>Fail Details</th>
            </tr>
            $Fail
        </table>
"""

not_implemented="""
        <h2>Not Implemented:</h2>
        <table id="no_implement" class="sortable">
            <tr>
                <th>$module</th>
                <th>$sys_module</th>
            </tr>
            $notImplemented
        </table>
"""
total_row="""
        <thead>
            <tr>
                <td>Total</td><td></td>$totalRow
            </tr>
        </thead>
"""

table_body="""
        <tbody>
            $tableBody
        </tbody>
"""

table_row="""
        <tr>
            $tableRow
        </tr>
"""

table_cell="""
        <td>$tableCell</td>
"""

table_cell_alink="""
        <td><a href="http://$localhostIp/$detail">Check Detail</a></td>
"""

