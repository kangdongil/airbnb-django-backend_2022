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
  # Modulize INSTALLED_APPS
  SYSTEM_APPS=[ ... ]
  CUSTOM_APPS=[ ... ]
  THIRD_PARTY_APPS=[ ... ]
  INSTALLED_APPS=SYSTEM_APPS+CUSTOM_APPS+THIRD_PARTY_APPS
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

## 1.0 Django Application
- App은 마치 Folder와 같다. 특정 주제의 Data와 그러한 Logic을 한 곳에 모아놓은 곳이다.
### 1.1 App을 Create하고 Configure하기
```shell
python manage.py startapp [APPNAME_PLURAL]
```
- App의 이름은 `복수형`으로 하는게 관행이다
- `apps.py`의 class(`~Config`)을 `config.settings`의 `CUSTOM_APPS`에 추가한다
  ```python3
    CUSTOM_APPS = [
      "users.apps.UsersConfig",
    ]
  ```
### 1.2 App Model를 Create하기
- `django.db.models`를 import하기
- `models.Model`을 inherit한 App Model을 Create하기
  ```python3
  from django.db import models

  class Room(models.Model):
    ...
  ```
### 1.3 App AdminPanel를 Configure하기
- `django.contrib.admin`를 import하기
- `admin.ModelAdmin`을 inherit한 App Admin을 Create하기
  - Model을 `@(Decorator)`로 언급하기
  ```python3
  from django.contrib import admin
  from . import models

  @admin.register(models.Room)
  class RoomAdmin(admin.ModelAdmin):
    ...
  ```

## 2.0 User App
- User App을 새로 처음부터 만들기보다 Django에서 제공하는 User App을 확장하는 게 효과적이다
- 첫 migration 전에 미리 Custom User를 세팅하는 것이 바람직하다.
- 만약 이미 어느정도 작업했다면 `db.sqlite3`과 `__init__`파일을 제외한 모든 각 App 폴더의 `migrations/` 파일을 삭제하고 Custom User를 세팅한다.
### 2.1 Custom User App 세팅하기
1. `users` App을 create하기
2. `AUTH_USER_MODEL`을 정하기
   - `config.settings`에 Django User를 inherit 받을 User App을 `AUTH_USER_MODEL`하겠다고 설정한다.
   ```
   AUTH_USER_MODEL = "users.User"
   ```
   - `django.contrib.auth.models.AbstractUser`을 import하기
3. `User Model` 만들기
   - Model의 경우, `models.Model` 대신에 `AbstractUser`을 inherit하기
   ```python3
   from django.contrib.auth.models import AbstractUser
   
   class User(AbstractUser):
     ...
   ```
4. `User AdminPanel` 만들기
   - `django.contrib.auth.admin.UserAdmin`을 import하기
   - Admin의 경우, `admin.UserAdmin` 대신에 `UserAdmin`을 inherit하기
   ```python3
   from django.contrib.auth.admin import UserAdmin
   from . import models
   
   @admin.register(models.User)
   class CustomUserAdmin(UserAdmin):
     ...
   ```
