## Clone 후 해야할 것
### 가상환경 생성
```
py -3.11 -m venv venv
```
### 가상환경 활성화
```
.\venv\Scripts\activate
```
### 라이브러리 설치
```
pip install -r .\requirements.txt
```
### DB 설정
```
flask db init
flask db migrate
flask db upgrade
```