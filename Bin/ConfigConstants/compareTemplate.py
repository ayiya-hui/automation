html_content="""
<html>
    <head>
        <style type="text/css">
            table { padding: 5px;
                    border-collapse: collapse;
                    border: 1px solid #000000;
                    width: 50%;
                    }
            td { border: 1px solid #000000;
                    padding: 3px;
                    font-size: .9em;
                    }
            th { border: 1px solid #000000;
                    background-color: #CCFFCC;
                    }
            .pg-normal {
                color: black;
                font-weight: normal;
                text-decoration: none;
                cursor: pointer;
            }
            .pg-selected {
                color: black;
                font-weight: bold;
                text-decoration: underline;
                cursor: pointer;
            }
        </style>
        <script type="text/javascript" src="paging.js"></script>
        <title>Accelops Compare Test Result</title>
    </head>
    <body>
        <h3>$description</h3>
        <hr>
        $content
    </body>
</html>
"""

compare_desc="""Compare test is performed on System $server1 and System $server2.\n
                System $server1 (Base) Version: $server1_version\n
                System $server2 Version: $server2_version\n
"""

content_body="""<h3>Module Name: $module_name</h3>
                <h4>Common: $common, Missing: $missing, Extra: $extra
                <table id="new_$module_name">
                    <tr>
                        <th>Name</th>
                        <th>Status</th>
                        <th>Reason</th>
                    </tr>
                    $table
                </table>
                <div id="pageNavPosition_$module_name"></div>
                <script type="text/javascript"><!--
                    var $module_name_pager = new Pager('new_$module_name', 50);
                    $module_name_pager.init();
                    $module_name_pager.showPageNav('$module_name_pager', 'pageNavPosition_$module_name');
                    $module_name_pager.showPage(1);
                //--></script>
"""

table_body="""
        <tbody>
            $tableBody
        </tbody>
"""

table_row="""
        <tr>
            <td>$name</td>
            <td>$status</td>
            <td>$reason</td>
        </tr>
"""
