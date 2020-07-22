# IZPM-Backup
**구독중인** 아이즈원 프라이빗 메일 백업 툴

```diff
- 실제 수신한 프라이빗 메일만 백업할 수 있습니다.
- 프라이빗 메일 유출을 위한 툴이 아닙니다.
- 백업의 결과물의 공유는 절대 금지합니다!!!
- 개발자는 본 툴의 이용에 있어 발생한 모든 문제에 대해 책임지지 않습니다.
```

## 준비물
Python + Requests

## 뭐하는 툴인가요
사용자가 수신한 모든 프라이빗 메일과 사진을 HTML 파일로 저장합니다. 

## 사용법
0. 본 repository를 clone 혹은 다운로드 합니다.
1. Burpsuite, Fiddler와 같은 HTTPS 프록시를 사용하여, 프라이빗 메일 패킷을 캡쳐합니다.
2. 패킷에서 아래 헤더 값들을 찾아, pm.py의 해당하는 변수에 값을 입력합니다.
 - User-Id : PM_USERID
 - Access-Token : PM_ACCESSTOKEN
 - Application-Version : PM_APPVER
 - Device-Version : PM_DEVICE
 - Os-Type : PM_OSTYPE
 - Os-Version : PM_OSVERSION
 - User-Agent : PM_USERAGENT
3. pm.py를 실행합니다. 모든 메일은 `output/mail` 폴더에 저장되며, 모든 이미지는 `output/image/mail`에 저장됩니다.
4. `output/viewer.html`을 실행하여 백업 결과물을 확인합니다.

**최신 버전의 Private Mail Viewer는 [BackupViewer](https://github.com/mdsnins/BackupViewer)를 확인해주세요.**

## 추가 예정인 기능
현재 버전은 멤버의 프로필 사진 다운로드를 지원하지 않습니다. 추후 추가될 예정입니다.
