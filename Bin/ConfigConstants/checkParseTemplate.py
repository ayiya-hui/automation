html_content="""
<html>
    <head>
        <script src="sorttable.js" type="text/javascript"></script>
        <style type="text/css">
            #new { padding: 5px;
                    border-collapse: collapse;
                    border: 1px solid #000000;
                    width: 50%;
                    }
            #new td { border: 1px solid #000000;
                       padding: 3px;
                       font-size: .9em;
                    }
            #new th { border: 1px solid #000000;
                       background-color: #CCFFCC;
                    }
            #old { padding: 5px;
                    border-collapse: collapse;
                    border: 1px solid #000000;
                    width: 50%;
                    }
            #old td { border: 1px solid #000000;
                       padding: 3px;
                       font-size: .9em;
                    }
            #old th { border: 1px solid #000000;
                       background-color: #00FFCC;
                    }
        </style>
        <title>Accelops Automation EventParsing Implementation Progess</title>
    </head>
    <body>
        <h2>Total $count. New Parsers of $new_count need to add to Automation</h2>
        <table id="new" class="sortable">
            <tr>
                <th>Module Name</th>
            </tr>
            $new
        </table>
        <hr/>
        <h2>Total $old_count Existintg Parsers are in Automation</h2>
        <table id="old" class="sortable">
            <tr>
                <th>Module Name</th>
            </tr>
            $old
        </table>
    </body>
</html>
"""

table_body="""
        <tbody>
            $tableBody
        </tbody>
"""

table_row="""
        <tr>
            <td><a href=$url>$module</a></td>
        </tr>
"""
