# IZPM-Backup
Backup your IZ\*ONE Private Mail with own credential

## Requirements
Python + Requests

## Usage
1. Use HTTPS proxy(Burpsuite, Fiddler, ...) to capture your own IZ\*ONE Private Mail packets
2. In HTTPS packet, extract below header values and write it down to python script
 - User-Id : PM_USERID
 - Access-Token : PM_ACCESSTOKEN
 - Application-Version : PM_APPVER
 - Device-Version : PM_DEVICE
 - Os-Type : PM_OSTYPE
 - Os-Version : PM_OSVERSION
 - User-Agent : PM_USERAGENT
3. Run python scripts, it will save all image files under `output/image/mail` folder, and mail contents under `output/mail` folder. Also, it will right simple javascript array file into `output/pm.js` for user who want to write your own viewer page


