#!/bin/bash

errorReportFile="errorReport"
compileReportFile="compileReport"

echo "Error Report >>>" > $errorReportFile

cp $PHOENIX_PATH/src/cpp/rule/userFuncDefs.xml .
$PHOENIX_PATH/src/cpp/rule/phRuleCompiler . >& $compileReportFile
rm userFuncDefs.xml

grep "WARNING\|ERROR,\|Compiling" $compileReportFile >> $errorReportFile
