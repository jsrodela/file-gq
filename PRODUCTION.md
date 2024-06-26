# 서버 설정 가이드

Ubuntu 20.04, Gunicorn, Nginx

### 가상머신 설정

1. 업데이트
```shell
sudo apt update
sudo apt upgrade
```

2. git clone
```shell
git clone https://github.com/jsrodela/file-gq.git
cd file-gq
```

3. 필요 프로그램 설치
```shell
# 파이썬 3.10 설치
sudo apt install python3.10.12
alias python=python3.10.12

# 가상환경 생성
sudo apt install python3.10.12-venv
python -m venv .venv
. .venv/bin/activate

# 의존 모듈 설치
pip install django

# 비밀키 설정
```shell
nano settings.json

# 아래 내용 입력
{
    "SECRET_KEY": "무작위 키" # 실제 서버 운영 시 유출 금지!!
}

# 컨트롤+V 후 엔터 누르고 나오기
```

4. 장고 설정
```shell
python manage.py makemigrations
python manage.py migrate
```

5. 서버 실행
```shell
python manage.py runserver
```
이제 `서버주소:8000`으로 접속해서 접속이 잘 되는지 확인한다. Azure의 네트워크 탭에서 포트 허용은 필수.

테스트가 완료되었다면 Ctrl+C를 눌러 서버를 닫아준다.

### Gunicorn 설정

1. Gunicorn 설치
```shell
# Gunicorn 설치
pip install gunicorn

# Gunicorn 테스트
gunicorn --bind 0:8000 main.wsgi:application
````
테스트에 성공하면 Ctrl+C로 서버를 닫아준다.


```shell
# 로그 파일 생성 (rodela 부분을 사용자 이름으로 바꿔서 실행)
sudo touch /var/log/gunicorn.access.log
sudo chown rodela:rodela /var/log/gunicorn.access.log
sudo touch /var/log/gunicorn.error.log
sudo chown rodela:rodela /var/log/gunicorn.error.log

# 호스트 등록
sudo nano /etc/systemd/system/gunicorn.service

# 아래 내용 입력
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=rodela
Group=rodela
WorkingDirectory=/home/rodela/file-gq
ExecStart=/home/rodela/file-gq/.venv/bin/gunicorn \
    --access-logfile /var/log/gunicorn.access.log \
    --error-logfile /var/log/gunicorn.error.log \
    --bind unix:/run/gunicorn.sock \
    main.wsgi:application
    
[Install]
WantedBy=multi-user.target

# 여기까지, 모든 rodela 부분을 사용자 이름으로 바꿔준다.
# 입력 끝났으면 Ctrl+X -> Y -> 엔터 로 나온다.

sudo nano /etc/systemd/system/gunicorn.socket

# 아래 내용 입력
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock
Socketuser=www-data

[Install]
WantedBy=sockets.target

# 입력 끝났으면 Ctrl+X -> Y -> 엔터 로 나온다.

# 시스템 이벤트 등록
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn.socket
systemctl status gunicorn.socket

# 접속 테스트
sudo -u www-data curl --unix-socket /run/gunicorn.sock http
# ALLOWED_HOSTS에서 걸리기 때문에, 오류가 뜨는 것이 정상이다.
```

### Nginx 설정

1. nginx 설치
```shell
sudo apt install nginx
nginx -v
```
서버에 접속해서 nginx가 설치되었는지 확인해보자. (포트 입력은 안해도 됨, Azure에서는 80번하고 443번 포트 열어놓기)

2. nginx 설정
```shell
sudo nano /etc/nginx/sites-available/main.conf
```
아래 내용을 입력한다.
```
server {
  listen 80;
  server_name jamsin-file.kro.kr;
  charset utf-8;
  client_max_body_size 1G;

  location /media {
    alias /home/rodela/file-gq/media;
  }

  location /static {
    alias /home/rodela/file-gq/static;
  }

  location /robots.txt {
    return 200 "User-agent: *\nDisallow: /";
  }

  location / {
    include proxy_params;
    proxy_pass http://unix:/run/gunicorn.sock;
    proxy_buffering off;
  }
}

server {
  server_name jamsin.kro.kr;
  return 301 https://jamsin-file.kro.kr$request_uri;
}
```

3. 설정 적용
```shell
# 설정 연동
sudo ln -s /etc/nginx/sites-available/main.conf /etc/nginx/sites-enabled/

# 설정 테스트
sudo nginx -t

# 설정 적용
sudo systemctl restart nginx
```
이제 서버주소로 접속하면 페이지가 로드될 것이다.

### SSL(https) 설정
```shell
# 업데이트
sudo snap install core
sudo snap refresh core

# certbot 설치
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot

# 인증서 발급
sudo certbot --nginx
```
이후 절차대로 진행. 설정 끝!

### 유용한 명령어
```shell
# 관리자 계정 생성
python manage.py createsuperuser

# 장고 출력 보기
nano /var/log/gunicorn.error.log
```
