## 0.0 개발환경 구축하기
### 0.1 Git 설정하기
- `git` 설치하기
- `cd [PROJECT_FOLDER]`
- `git init`
- `touch .gitignore`
  - [Python_GitIgnore](https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore)
- `git add . && git commit --amend --no-edit`
- `git remote add origin [REPOSITORY_URL}`
- `git push origin main --force`

### 0.2 Python 3.8^ 설치하기
- `Local`
- `GitPod` - Default(3.8.13)
- `GoormIDE`
  ```shell
  sudo apt update && sudo apt install -y python3.8 && sudo update-alternatives --install /usr/local/bin/python3 python3 /usr/bin/python3.8 0
  ``` 

### 0.3 Python Virtual Environment 설정하기: Poetry
1. CLI로 설치하기
  ```shell
  curl -sSL https://install.python-poetry.org | python3 -
  ```
2. `poetry init`
3. `poetry shell`

#### 0.3.1 Poetry 살펴보기
- `poetry init`: 프로젝트를 poetry가 관리하게 하기
- `poetry add [PACKAGE]`: poetry로 python package 설치하기
- `poetry add --dev [PACKAGE]`: 개발자전용 package 설치하기
- `poetry shell`: shell 진입하기
- `exit`: shell 나가기
- `pyproject.toml`: 프로젝트의 명세와 의존성 관리하는 파일

### 0.4 Django Project 시작하기
- `poetry add django`
- `django-admin startproject config .`

#### 0.4.1 Django Project 구조 살펴보기
- `manage.py`
  - Terminal에서 Django 명령을 실행하게 함
- `db.sqlite3`
  - Development 단계에서 Django가 임시로 사용하는 DB 파일
  - 첫 `runserver` 명령과 함께 자동으로 빈 파일로 생성됨
  - `migration`을 통해 코드에 알맞은 DB 모양이 되도록 동기화함.
- `config/`
  - `config.settings`
    - Django Project 관한 모든 설정이 이뤄지는 파일
  - `config.urls`
    - Django Project의 Url들을 관리하는 파일
    - `include`로 App별 url을 묶어 관리하기 좋다

### 0.4.1 Django Project 설정하기
- `config.settings`
  ```python3
  # Allow Gitpod To run Django Server
  ALLOWED_HOSTS = ["localhost"]
  CSRF_TRUSTED_ORIGINS = ["https://*.ws-us72.gitpod.io"]
  # To use Server Timezone
  TIME_ZONE = "Asia/Seoul
  ```

### 0.4.2 Django Project Command(`manage.py`) 사용하기
  - `python manage.py [COMMAND]`
  - `runserver`: Django 서버 시작하기
  - `createsuperuser`: Admin 계정 만들기
    - admin 계정을 저장할 DB와 migration이 필요하다
    - DB를 초기화(삭제)할 때마다 admin 계정을 새로 만들어야 한다
  - `makemigrations` >> `migrate`: Model의 변경사항을 DB에 반영하는 행위
    - 세부적으로 `makemigrations`은 파일생성,   
      `migrate`는 변경된 내용을 적용한다.
  - `shell`: Django Shell 켜기
    - `ORM` 등 Django 코드를 콘솔에서 테스트하기 좋다

### 0.5 Django Server 시작하기
1. `python manage.py runserver`
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. `python manage.py createsuperuser`
5. `/admin` 접속하여 admin 계정으로 로그인하기
6. `Admin Panel`을 접속했다면 서버 준비완료