# IZPM-Backup
**구독중인** 아이즈원 프라이빗 메일 백업 툴

기존 버전을 확인하시려면 `legacy` 브랜치 혹은 [./legacy](legacy) 폴더를 확인해주세요.


## 일반 사용자들

***Android용 매뉴얼은 추후 작성 예정입니다.***

1. 상단의 초록색 **Code** -> **Download Zip**을 클릭하여 다운로드 받고 압축을 푼 후, `user` 폴더만 남깁니다.
1. 사용하는 iOS 단말기에서 Wi-Fi에 연결합니다.
1. Wi-Fi 옆 (i) 아이콘을 누르고, 아애로 스크롤을 내려 프록시 구성 > 수종 > 서버 `izpm.wonyoung.kr`, 포트 `1029`를 입력합니다.
1. Safari 브라우저를 이용하여 주소창에 `http://private.mail`에 접속합니다.
1. 사이트 중앙에 있는 iOS 밑 `Get mitmproxy-ca-cert.pem` 초록색 버튼을 클릭합니다.
1. 알림창이 뜨면 허용을 클릭합니다.
1. 설정 앱 메인의 `프로파일이 다운로드됨`에서 프로파일을 설치합니다.
1. 설정 앱의 `일반 > 정보` 하단의 `인증서 신뢰 설정`에서 `Private Mail CA`를 활성화 합니다.
1. 이후 `프라이빗 메일` 앱으로 이동합니다.
1. 아무 메일이나 클릭하여 나오는 키와 PIN을 기록합니다. 이 때, 키는 멤버 이름 + 무작위 숫자 4자리, PIN은 무작위 숫자 4자리로 구성됩니다.
1. 컴퓨터에서 [http://izpm.wonyoung.kr](http://izpm.wonyoung.kr)에 접속합니다.
1. 접속 후, 나오는 입력창에 키와 PIN을 입력합니다.
1. 받아지는 Python 스크립트를 실행합니다.
1. 실행 후 `output` 폴더의 내용물을 `1번`의 `user` 폴더로 이동시킵니다.
1. `user` 폴더의 `viewer.html`을 더블클릭 하여 브라우저로 실행합니다.


## 프로그래머용 (자체 서버 구성)


```sh
git clone https://github.com/mdsnins/IZPM-Backup/
```

`docker-compose.yml` 파일을 본인 환경에 맞게 수정 후

```sh
docker-compose up -d
``` 

