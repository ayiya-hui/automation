#!/bin/bash

template=$1

errorReportFile=$template"-errorReport"
compileReportFile=$template"-compileReport"

#echo $errorReportFile

echo $template
echo "Error Report >>>" > $errorReportFile

cp $PHOENIX_PATH/src/cpp/rule/userFuncDefs.xml .
$PHOENIX_PATH/src/cpp/rule/phRuleCompiler $template >& $compileReportFile
rm userFuncDefs.xml

grep "ERROR,\|Compiling" $compileReportFile >> $errorReportFile
