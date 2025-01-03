# file-gq
파일 공유와 전송을 보다 간단하게

## 사용법
1. 왼쪽 파일 목록에서 파일을 선택하고, 코드를 작성한다.
2. 위쪽의 Run 버튼을 눌러 서버를 실행하고, 아래 주소로 들어간다. https://file-gq-1.rodela6.repl.co/ (replit의 webview로 보는 것보다 다른 탭에서 링크로 들어가서 보는걸 추천)
3. 새로고침과 코드 수정을 반복한다. 화이팅! (F5로 적용 안되면 Ctrl+F5 눌러보기)
4. 수정한 내용을 아래 '수정 기록'에 남겨두기

여러분이 이 프로젝트의 주인입니다! 아이디어가 있다면 거리낌 없이 수정해주세요. 특정 기능을 넣고 싶은데 잘 안되면 언제든지 물어보세요 - 함께하기 위해 우리가 로델라에 있는 겁니다!

## 서버 설정
   [PRODUCTION.md](PRODUCTION.md)

## 파일 구조
- fileapp : 파일 공유와 관련된 모든 것들 
- main : 최상위 프로젝트

  - urls.py : 특정 주소로 들어왔을 때 실행할 함수 설정
  - views.py : 사용자의 요청을 처리하여 HTML 파일을 반환하는 함수
  - templates / HTML.html : views.py에서 반환될 HTML 파일
  - static / 파일 : HTML에서 불러올 CSS & JavaScript 코드, 혹은 이미지 파일 등

## 링크 구조
- `/` : 메인 페이지
- `/send` : 보내기
- `/send_result` : 보내기 결과, 보낸 후 QR코드랑 숫자 표시하는 페이지
- `/receive` : 받기
  
## Requirements
만약 poetry 쓰기 힘들다면, pip으로 아래 라이브러리만 설치해주자
* django

참고로 `SECRET_KEY` 가 설정되어 있어야 동작한다.
```shell
nano settings.json

# 아래 내용 입력
{
    "SECRET_KEY": "무작위 키" # 실제 서버 운영 시 유출 금지!!
}

# 컨트롤+V 후 엔터 누르고 나오기
```

gunicorn.service 설정할때는 환경변수를 다음과 같이 설정해준다.
```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=rodela
Group=rodela
Environment="SECRET_KEY=RODELA_SECRET"
WorkingDirectory=/home/rodela/file-gq
ExecStart=/home/rodela/file-gq/.venv/bin/gunicorn \
    --bind unix:/run/gunicorn.sock \
    main.wsgi:application

[Install]
WantedBy=multi-user.target
```

nginx 설정할때 media는 [이 링크](https://stackoverflow.com/questions/9054354/how-to-force-file-download-in-the-browser-nginx-server) 참고해서 force download되도록 해두기 (참고로 아이폰에서 다운로드가 잘 안되는데, 문제가 뭔지 모르겠어서 찾으면 좋을듯)

## 수정 기록

5/14
- 메인, 보내기, 결과, 받기 페이지 추가 / 강이규

5/28
- CSS 분리 / 강이규
- 버튼 호버기능 추가 / 강이규

5/31
- 디버그 / 강이규
- 버튼 텍스트, 사각형 병합 / 강이규
- 배경 도형 추가, 색상 변수화 / 강이규
- 프론트엔드팀에서 상의한 것과 같이 디자인 변경 / 강이규
- 
6/1
- 배경 색상 더 진하게 변경 / 김정윤
- send페이지 form 추가, urlpatterns name 추가, models 추가 / 박도현

6/2
- send에서 파일 업로드 버튼 위치 수정/홍채이

6/3
- views.send() 내용 임시, send페이지 form 수정
- media root 설정, admin 추가 / 정현석

6/30
- 파일 받기 백앤드 기능 추가 / 정현석

7/8
- 디자인 다듬기 / 강이규

7/9
- 파일 받기 코드를 입력하지 않고 GO 버튼을 눌렀을 때 오류가 발생하는 현상 수정 / 윤지욱
- 체크박스 추가 / 강이규
- 코드 입력창 증감 버튼 제거, 공유코드 밑으로 밀리는 오류 수정, qr에 링크 포함, 모바일 화면 / 정현석

7/10
- 레이아웃 개선, 카톡 미리보기 설명 추가, 랜덤 색상 기능 / 정현석

???
- purple 추가 / ???

7/17
- 사이트 이름 jamsin.tk로 변경 / 정현석

7/30
- 글꼴 롤백 / 강이규

24/2/7
- 배포 가이드 추가, 설정파일 URL 업데이트 / 윤지욱

24/5/13
- settings.json 분리, 인생네컷 지원 분기 / 윤지욱
