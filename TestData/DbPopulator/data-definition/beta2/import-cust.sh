#!/bin/sh
if [ $# -lt 2 ]; then
         echo 1>&2 Usage: $0 ServerIP customer-xml-data
         exit 127
fi

/opt/phoenix/deployment/prepopulator.sh $1 User $2
/opt/phoenix/deployment/phoenixCLI.sh $1
