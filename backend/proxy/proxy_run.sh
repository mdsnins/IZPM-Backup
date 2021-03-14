#!/bin/sh
./certgen.sh
mv cert /cert
mitmdump --set onboarding_host=private.mail --set confdir=/cert/ --set block_global=false -p 1029 -s service.py > /dev/null