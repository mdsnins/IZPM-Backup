#!/bin/sh
cd /tmp/
./certgen.sh
mv cert /cert
rm certgen.sh
mitmdump --set cert_passphrase=$AES_PASS --set onboarding_host=private.mail --set confdir=/cert/ --set block_global=false -p 1029 -s /app/service.py > /dev/null
