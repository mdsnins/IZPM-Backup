#!/bin/sh
openssl genrsa -aes256 -passout env:AES_PASS -out cert.key 4096
openssl req -new -x509 -days 365 -key cert.key -passin env:AES_PASS -out cert.crt -subj "/C=CA/O=IZPMBackup/OU=IZ*ONE Private Mail Backup Service/CN=Private Mail CA/"
openssl pkcs12 -export -passin env:AES_PASS -out cert.p12 -passout env:CA_PASS -inkey cert.key -in cert.crt
cat cert.key cert.crt > mitmproxy-ca.pem
openssl pkcs12 -in cert.p12 -passin env:CA_PASS -clcerts -nokeys -out mitmproxy-ca-cert.pem
cp mitmproxy-ca-cert.pem mitmproxy-ca-cert.cer
rm -f cert.key cert.crt cert.p12
mkdir cert
cp mitm* cert/
