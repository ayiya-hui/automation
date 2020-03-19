"""This file contains information for creating query template."""

query_xml="""<Reports><Report id="automation" group="automation">
     <Name>Automation Query</Name>
     <Description>This is for Automation script to query data.</Description>
     <CustomerScope groupByEachCustomer="true">
          <Include all="true"/>
          <Exclude/>
     </CustomerScope>
     <SelectClause numEntries="All">
          <AttrList/>
     </SelectClause>
     <OrderByClause>
          <AttrList/>
     </OrderByClause>
     <PatternClause window="3600">
          <SubPattern displayName="automation" name="automation">
               <SingleEvtConstr>$constr</SingleEvtConstr>
          </SubPattern>
     </PatternClause>
     <ReportInterval>
          <Window unit="Minute" val="$minute" />
     </ReportInterval></Report></Reports>"""

xml_escapes=(('&','&amp;'),
             ('<','&lt;'),
             ('>','&gt;'))

str_escapes=(('\\','\\\\'),
             ('"','\\"'))
			 







