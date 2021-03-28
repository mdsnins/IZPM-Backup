# IZPM-Backup
**구독중인** 아이즈원 프라이빗 메일 백업 툴

HTTPS 프록시 서버와 연계하여, 사용자가 패킷을 수동으로 캡처할 필요 없이 자동 구성된 스크립트 다운로드를 지원합니다.

혹시 실행에 문제가 있는 경우, 본 문서 하단의 FAQ 항목에 본인의 문제가 있는지 확인 해주세요.

현재 실행 스크립트의 가장 최신 버전은 `2.5.0`입니다. 버전별 변경 사항은 [버전정보](./VERSION.md)를 참고 해주세요.

가이드 링크 (03.17 기준)

- **iOS** : [장원영갤러리 - iOS 프메 백업 가이드](https://gall.dcinside.com/mgallery/board/view/?id=wonyeong&no=368368)
- **Android with Custom APK** : [장원영갤러리 - Android 프메 백업 가이드](https://gall.dcinside.com/mgallery/board/view/?id=wonyeong&no=368388)
- **Android with Nox** : [최예나갤러리 - 안드로이드 대충 원클릭](https://gall.dcinside.com/mgallery/board/view/?id=chaeyaena&no=552474&page=1)

## 일반 사용자들

### iOS User
1. 상단의 초록색 **Code** -> **Download Zip**을 클릭하여 다운로드 받고 압축을 푼 후, `user` 폴더만 남깁니다.
1. 사용하는 iOS 단말기에서 Wi-Fi에 연결합니다.
1. Wi-Fi 옆 (i) 아이콘을 누르고, 아애로 스크롤을 내려 프록시 구성 > 수동 > 서버 `izpm.wonyoung.kr`, 포트 `1029`를 입력합니다.
1. Safari 브라우저를 이용하여 주소창에 `http://private.mail`에 접속합니다.
1. 사이트 중앙에 있는 iOS 밑 `Get mitmproxy-ca-cert.pem` 초록색 버튼을 클릭합니다.
1. 알림창이 뜨면 허용을 클릭합니다.
1. 설정 앱 메인의 `프로파일이 다운로드됨`에서 프로파일을 설치합니다.
1. 설정 앱의 `일반 > 정보` 하단의 `인증서 신뢰 설정`에서 `Private Mail CA`를 활성화 합니다.
1. 이후 `프라이빗 메일` 앱으로 이동합니다.
1. 아무 메일이나 클릭하여 나오는 키와 PIN을 기록합니다. 이 때, 키는 멤버 이름 + 무작위 숫자 4자리, PIN은 무작위 숫자 4자리로 구성됩니다.
1. 컴퓨터에서 [http://izpm.wonyoung.kr](http://izpm.wonyoung.kr)에 접속합니다.
1. 접속 후, 나오는 입력창에 키와 PIN을 입력하여 `config.json`을 다운로드 받습니다.
1. 페이지에서 `izpm_run.py`를 다운로드 합니다.
1. `izpm_run.py`와 `config.json`을 같은 폴더에 놓고, `izpm_run.py`를 실행합니다.
1. `output` 폴더의 `viewer.html`을 더블클릭 하여 브라우저로 실행합니다.

### Android User
1. [http://izpm.wonyoung.kr/apk](http://izpm.wonyoung.kr/apk)에서 수정된 Private Mail 앱을 다운로드 받습니다.
1. 수정된 Private Mail 앱의 정상 동작을 확인합니다.
1. 이후, 호스트 `izpm.wonyoung.kr` 포트 `1029`로 프록시를 설정합니다.
1. `http://private.mail`에 접속하여 Android용 인증서를 설치합니다. (운영체제, 제조사별 설치방법 상이)
1. iOS 유저 가이드의 9번 항목으로 이동하여 진행합니다.


## 프로그래머용 (자체 서버 구성)


```sh
git clone https://github.com/mdsnins/IZPM-Backup/
```

`backend/docker-compose.yml` 파일을 본인 환경에 맞게 수정 합니다.<br>
이어, `backend/web/page/`에 수정한 `izonemail.apk`를 복사 후

```sh
docker-compose up -d
``` 

## FAQ

### JSON 관련 에러가 나와요

신규 버전으로 업데이트 된 이후, `pm.js` 저장 방식에 차이가 생겨서 그렇습니다. 기존 `pm.js`를 지우고 실행해주세요.

### No module named requests

requests 라이브러리를 설치해주세요. pip, easy_install 등을 통해 설치할 수 있습니다. 구글에 상당한 양의 매뉴얼이 있습니다.

### CA 인증서 설치가 안돼요. (안드로이드)

설정 앱에서 수동으로 인증서 설치를 시도해보세요.

### 프록시 설정 이후 인터넷이 안돼요 (iOS & 안드로이드 공통)

정상입니다. 인증서가 정상적으로 설치되기 전까지는 인터넷 연결이 원활하지 않을 수 있습니다.
