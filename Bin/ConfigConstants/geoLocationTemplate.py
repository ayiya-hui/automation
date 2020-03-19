html_content="""
<html>
    <head>
        <script src="sorttable.js" type="text/javascript"></script>
        <style type="text/css">
            #new { padding: 5px;
                    border-collapse: collapse;
                    border: 1px solid #000000;
                    width: 100%;
                    }
            #new td { border: 1px solid #000000;
                       padding: 3px;
                       font-size: .9em;
                    }
            #new th { border: 1px solid #000000;
                       background-color: #CCFFCC;
                    }
        </style>
        <title>Accelops Automation Geo Location Testing</title>
    </head>
    <body>
        <b1>Geo Location from Accelops and Web</b1>
        <table id="new">
            <tr>
                <th>IP Address</th>
                <th>Organization</th>
                <th>City</th>
                <th>State</th>
                <th>Country</th>
                <th>Latitude</th>
                <th>Longtude</th>
            </tr>
            $new
        </table>
    </body>
</html>
"""
table_body="""<tbody>$tableBody</tbody>"""
table_row="""<tr>$row_value</tr>"""
table_cell="""<td>$cell_value</td>"""

