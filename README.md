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
#### 1.2.1 Model Field와 종류 살펴보기
- `Field`는 models의 메서드로 특정 속성을 가진 데이터형을 제시한다.
```python3
class Model([]):
  [FIELD] = models.[FieldType](~)
```
- 짧은 텍스트는 `CharField`로 하고, `max_length`를 필수로 가진다
- 긴 텍스트는 `TextField`를 사용한다
- 참거짓값은 `BooleanField`, 양의 정수값은 `PositiveIntegerField`를 사용한다
- 이미지파일은 `ImageField`를 사용하며 파이썬 패키지 `Pillow`를 필요로 한다
- `DateTimeField`는 날짜시간을 표현한다
  - 날짜만 `DateField`, 시간만 `TimeField`
  - `auto_now_add=True`: 처음 생성된 날짜
  - `auto_now=True`: 마지막으로 업데이트한 날짜
#### 1.2.2 `Default` / `Blank` / `Null`
- `Default`는 Client가 값을 입력하지 않았을 때 주는 기본값이며,   
  기존 데이터가 새로운 Field가 추가되었을 때 가지는 값이기도 하다
- `Blank`는 Client 측에서 Form Input을 비웠을 때 허용하는지 여부를 정한다
- `Null`는 DB 측에서 Null값을 허용하는지 여부를 정한다
#### 1.2.3 Model 형태가 달라지면 Migration하기
- Model을 새로 만들거나 수정하였을 때,   
  해당 코드에 맞게 DB형태를 바꾸는 과정을 `migration`이라 한다.
- `python manage.py makemigration`과 `python manage.py migrate`을 연이어 적용한다.
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
### 1.3.1 AdminPanel Option 살펴보기
- `list_display`: Admin Panel에 보여줄 Column 속성들을 튜플로 정의하기
```python3
list_display = ("[Field]", ...)
```
- `list_filter`: Admin Panel 우측에 제공할 필터를 튜플로 정의하기
```python3
list_filter = ("[Field]", ...)
```
- `fieldsets`: Admin Panel에서 Data를 생성 또는 수정하는 화면 구성을 정의하기
```python3
fieldsets = (
  ("[Section_Title]", {
    "fields": (~),
    "classes": (~),
  }),
  ...fieldset
)
```
  - `fieldset`: 큰 Section으로 튜플로 정의한다
  - `fields`: Admin Panel에서 다룰 Model Field 정의하기
  - `classes`: FieldSet을 CSS 옵션을 추가한다
    - `wide`: 화면을 더 넓게 사용하기
    - `collapse`: fieldset을 접을 수 있게 한다
  - 항목이 하나인 튜플에 `,`을 넣어 포맷팅으로 사라지는 오류를 방지하자
  ```python3
  {"fields": ("name",),}
  ```
- `search_fields`: 좌상측에 키워드로 검색하여 항목을 조회할 수 있다
  - `search_fields = ("[COND1]", "[COND2]")`
  - `search_help_text`로 검색창 하단에 설명을 넣을 수 있다
  - `lookups`을 삽입하여 `contains`가 아닌 다른 옵션을 설정할 수 있다
    - `^`(startswith)
    - `=`(exact)
  ```python3
  search_fields = (
    "owner__username",
    "=price",
  )
  search_help_text = "~"
  ```
- `actions`: 좌상측에 일괄처리 항목을 선택할 수 있다
  - `actions.py`을 만들어 별도로 관리할 수 있다 혹은 `admin` 안에 포함시킬 수 있다
  - `Custom Action` 정의하기
    ```python3
    @admin.action(description="~")
    def [custom_action](model_admin, request, instances):
      for instance in instances.all():
        ...
        instance.save()
    ```
  - `Admin`에 `actions` 포함시키기
    ```python3
    from .actions import [custom_action]

    @admin.register(Model)
    class Admin(admin.ModelAdmin):

      actions = ([custom_action], ...)
    ```

### 1.4 Abstract Model 사용하기
1. `Common` App을 Create하기(Optional)
```bash
django-admin startapp common
```
  - `config.settings`에 `CommonConfig`을 `CUSTOM_APPS`에 추가하기
2. `TimeStampedModel`을 Create하기
  - `created`와 `updated`를 `DateTimeField`로 하기
    - `created`: `auto_now_add`를 `True`하기
    - `updated`: `auto_now`를 `True`하기
3. 내부클래스 `class Meta`에 `abstract=True`하기
```python3
class TimeStampedModel(models.Model):
  class Meta:
    abstract=True
```
  - `abstract=True`하면 해당 Model은 DB에 저장되지 않는다
4. 해당 `Abstract Model`을 `import`하여 사용할 Class에 `inherit`하기
```python3
from common.models import TimeStampedModel

class Model(TimeStampedModel):
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

### 2.2 User Model 만들기
- [`AbstractUser`](https://github.com/django/django/blob/main/django/contrib/auth/models.py#L334-L402)가 가진 field를 참고하기
- 기존의 `first_name`과 `last_name`은 사용 안하도록 `editable`을 `False`하기
- 입력이 아닌 선택지를 주려면 `CharField`에 `choices` 항목을 주기
  ```python3
  gender = models.CharField(
    max_length=5,
    choices=GenderChoices.choices,
    default=GenderChoices.MALE,
  )
  ```
- Choices는 내부클래스로 정의한다
  - `django.db.models.TextChoices`를 inherit한다
  - 변수명은 `UPPERCASE`로 정하고, 튜플 안에 첫번째 항목은 DB에 저장되는 값으로 `lowercase`를, 두번째 항목은 Client가 보는 항목으로 `TitleCase`로 표기한다
  ```python3
  class GenderChoices(models.TextChoices):
    MALE = ("male", "Male")
    ...
  ```
### 2.3 User Admin 만들기
- [`UserAdmin`](https://github.com/django/django/blob/main/django/contrib/auth/admin.py#L43-L83) 참고하기
- `fieldsets`을 설정하여 기존 UserAdmin의 항목을 확장한다

## 3.0 Project에 필요한 App 만들기
### 3.1 Room App & Amenity Model
- `Room`은 여러 `Relationship`을 가진다.   
  User `owner`은 `Room`을 소유하며(`ForeignKey`),   
  `Room`들은 여러 `Amenity`를 가진다(`ManyToManyField`)
- `__str__`을 수정하여 `Room`이 Admin Panel에 어떻게 표현되는지 수정한다
- Admin Panel은 단수형 Model 이름에 단순히 `-s`를 붙여 복수형을 표현한다. 따라서 `Amenities`의 경우 복수형을 직접 표현해주어야 한다
- inherit한 Abstract Model의 Field를 Admin Panel에 드러나게 만들어보자(`read_only`)
### 3.1.1 Room Model을 Create하기
- `ForeignKey`는 `연결할 모델`과 `연결된 모델이 삭제되었을 때 대응`을 언급해야 한다
  - `연결할 모델`은 다음과 같은 방식으로 표시한다
    - `같은 파일 내 모델`의 경우,
    ```python3
    models.ForeignKey("model", on_delete=models.CASCADE)
    ```
    - `다른 App의 모델`의 경우,
    ```python3
    models.ForeignKey("app.model", on_delete=models.CASCADE)
    ```
  - `on_delete`로 연결된 모델이 삭제되었을 때 대응을 정한다
    - `models.CASCADE`: 함께 삭제된다
    - `models.SET_NULL`: 내역이 남는다(`Null=True` 함께 사용)
### 3.1.2 Room Admin을 Configure하기
1. `Reverse Accessor`
  - `ForeignKey`나 `ManyToManyField`는 역으로 Model을 접근할 수 있는데 이는 기본적으로 `_set`라는 이름 가진다
  ```python3
  class User(~):
    ...
    rooms = self.room_set.count()
  ```
  - 예를 들어, 각 room은 `host`를 가지는데, host는 여러 `rooms`를 가질 수 있다. 이때 이 `room_set`은 User 입장에서 `self.room_set`으로 접근 가능하다
  - `Reverse Accessor`가 보다 직관적인 이름을 가지도록 하려면 `related_name`으로 항목을 준다
  ```python3
  # rooms/models.py
  class Room(~):
    ...
    host = models.ForeignKey(
      "users.User",
      on_delete=models.CASCADE,
      related_name="rooms",
    )
  # users/models.py
  class User(AbstractUser):
    ...
    rooms = self.rooms.count()
  ```
2. `Model Method`
  - `Model Class`이나 `Admin Class`는 `Method`를 가질 수 있다
  - `Method`는 Class 속 `Function`으로 DB에서 처리한 값을 return하는데 사용한다.
  - Model Method는 `self`를 첫번째 인자로 가진다. `self`는 직관적으로 Model 이름을 가져도 좋다.
3. `ORM`으로 Room Amenities의 합계 구하기
  - `ORM`(Object Relational Mapper)로 python 코드로 DB를 CRUD할 수 있다.
  - `ORM`을 통해 얻은 DB 결과는 `QuerySet` 형태를 띄며, 이를 통해 여러 작업을 할 수 있다. 총합은 `.count`를 사용한다
  ```python3
  class Room(~):
    ...
    def total_amenities(room):
      return room.amenities.count()
  ```

* `ORM` 예시
  - `.objects.all()`: 해당 model의 모든 Instance를 불러온다
  - `[QUERYSET].count()`: 해당 QuerySet 안의 Instance 갯수를 return한다.
### 3.1.3 Amenity App & Admin를 Create하기
- `ManyToManyField`는 1대多 관계를 표현한다.
  ```python3
  models.ManyToManyField("app.model")
  ```
- `AdminPanel`에서 복수형 표현을 수정해야 한다면,
  - `class Meta`로 `verbose_name_plural` 이용하기
  ```python3
  class Amenity(Model):

    class Meta:
      verbose_name_plural = "~"
  ```
- `readonly`한 field를 AdminPanel 수정창에 뜨도록 하려면,
  - `readonly_fields`에 표시한다
  ```python3
  readonly_fields = ("~", ...)
  ```

### 3.2 Experience App & Category App
- `Room` App과 같은 전개로 만들어가되 숙박 개념이 없는 experience는 당일 `시작시간`과 `종료시간`을 가지도록 한다
- `Room`의 부속시설인 `Amenity`처럼 `Experience`는 `Perk`을 `ManytoManyField`로 가진다.
- `Category`는 `Room` 또는 `Experience`의 그룹이다

### 3.3 Review App
- `__str__` 메서드가 return할 값을 customize할 수 있다. `f"" String`을 활용해 변수들을 `{~}`에 넣어 표현 가능하다.
  ```python3
  def __str__(self):
    return f"{self.user} / {self.rating}"
  ```
- Room Reviews들의 평균(Average)을 구하는 Class Method을 만든다
  - `산술평균`: $\frac{(Review Ratings의 총합)}{(Reviews 갯수)}$
  - 해당 Room의 `Review` 갯수 구하기
    - `self.reviews.count()`
  - `Review` 갯수가 `0`일 때 예외처리하기
  - Review Ratings의 총합 구하기
    - 모든 reviews에서 rating만 가져오기
    - `self.reviews.all().values("rating")`
    - `for문` 돌려서 rating값 누적합하기
  - `return`할 때 소수점 아래 두자리 반올림하기(`round`)
- `list_filter`는 단순히 해당 Model의 Field만 가능한게 아니라 `__`로 다른 ForeignKey로 접근한 다른 Model의 Field도 기준으로 삼을 수 있다.
  ```python3
  list_filter = (
    "user__is_host",
    "room__category",
  )
  ```
- `Custom Filter`를 만들어 이를 `list_filter`에 기재할 수 있다.
  - `django.contrib.admin.SimpleListFilter`를 import하기
  - `admin.py`에 inline으로 작성해도 좋고 `filter.py`를 별도로 만들어 관리할 수 있다.
  ```python3
  class CustomFilter(SimpleListFilter):
    title = "~"
    parameter_name = "~"

    def lookups(self, request, model_admin):
      return [("PARAM_VALUE", "CLIENT_NAME"), ...]
    
    def queryset(self, request, queryset):
      param = self.value()
      match = {
        "PARAM_VALUE": queryset.filter(~),
        ...
      }
      return match.get(param, queryset)
  ```
  - `title` / `parameter_name` 값을 입력한다
    - `title`은 Admin Panel 우측 Filter칸에 Filter 이름을 말한다
    - `parameter_name`은 URL에서 parameter 이름을 무엇으로 할지 정한다
  - `lookups` Function은 Client에게 Filter에 어떻게 보일지 정하는 것이다.
  - `queryset` Function은 param에 따라 제시할 queryset을 filter하여 제시한다.
    - `.get`은 param이 있을 때 `match` Dictionary를 참고하지만, 없다면 전체 queryset을 돌려준다
- `Custom Filter`를 `admin.py`에 `import`하고 `list_display`에 추가한다

## 4.0 Django Url & Django View
### 4.0.1 Django가 웹을 구현하는 과정
- Django가 BackEnd에서 FrontEnd로 Data를 구현할 때,   
  다음 3단계를 거친다   
  `Model` + `Url` - `View` - `Template`
  - `Model`은 DB에 담긴 data에 대한 정의를 말한다
  - `Url`은 Client가 접속하는 Url을 정의하고 처리하는 함수를 연결해준다
  - `View`는 Url을 접속할 때 Response를 처리하는 함수이다
  - `Template`은 Response한 응답한 HTML이다
- 이번 프로젝트에서는 `Django Template`을 사용하지 않고 `React`로 FrontEnd를 구현할 것이다
- 따라서, `Template` 대신 data를 json으로 구현할 `API`로 Response 하겠다
### 4.1 Django Url
- `config/urls.py`
  1. `django.urls`에서 `path`와 `include`를 `import`하기
  ```python3
  from django.urls import path, include
  ```
  2. `urlpatterns`라는 `list`(`[]`)를 만들어 `path`들을 관리한다.
  ```python3
  urlpatterns = [
    path(~),
  ]
  ```
  3. 각 app폴더마다 `url`을 따로 관리하는 경우에는,   
  `path`에 `url`과 `[apps].urls` 경로가 포함된 `include`를 넣는다.
  ```python3
  path("rooms/", include("rooms.urls"))
  ```
- `[apps]/urls.py`
  1. `django.urls.path`와 `views.py` 내 모든 view들을 `import`한다
  ```python3
  from django.urls import path
  from . import views
  ```
  2. `urlpatterns`을 만들고 `path`에 `include` 이후 이어지는 `url`과 `view`를 적는다
  ```python3
  urlpatterns = [
    path("", views.rooms),
    ...
  ]
  ```
  3. `FBV`(Function-based View)가 아닌 `CBV`(Class-based View)를 채택한다면 `.as_view()`를 덧붙인다
  ```python3
  path("", views.Room.as_view())
  ```
  4. Url에 변수를 주려면 `<[DATATYPE]:[PARAM_NAME]>`로 표현한다.
  ```python3
  path("<int:pk>", views.RoomDetail.as_view())
  ```
### 4.2 Django View
- 모든 `View` function은 첫번째 인자로 `request`를 가진다
- `URL`에 `변수`를 주면 View Function은 인자를 받을 수 있다
  ```python3
  # urls.py
  path("<int:pk>", views.~)
  # views.py
  def room(request, pk):
    ...
  ```
- `Json`을 return하는 `View`를 만드려면 다음 사항이 필요하다
  ```python3
  from django.http import HttpResponse
  from django.core import serializers

  def rooms(request):
    queryset = Room.objects.all()
    data = serializers.serialize("json", queryset)
    return HttpResponse(content=data)
  ```
  1. `QuerySet`을 가져온다
  2. `Serializer`로 `QuerySet`을 `Json`으로 변환한다
  3. `Json`화된 data를 `Response`로 `return`한다

## 5.0 Django REST Framework로 API 만들기
### 5.1 DRF 설치하기
1. `Poetry`로 `DRF` 설치하기
  ```shell
  poetry add djangorestframework
  ```
2. `config.settings`에서 `THIRD_PARTY_APPS`에 DRF를 등록하기
  ```python3
  THIRD_PARTY_APPS = ["rest_framework",]
  ```
3. DRF를 사용할 `views.py`에 `import`하기
  ```python3
  import rest_framework

### 5.2 DRF로 Function-based View(FBV) 만들기
1. `DRF Response`
  - `rest_framework.response.Response`로 import하기
  ```python3
  def view(request):
    ...
    return Response([JSON])
  ```
2. `DRF Serializer`
  - `rest_framework.serializers.Serializer`를 import하기
  - `serializers.py`를 만들어 관리하기
  - serialize할 `model`를 import하고 json에 포함할 `field`를 맞대응하여 추가한다
    - `serializers.ModelField(~)`식으로 추가한다
3. `@api_view`
  - `rest_framework.decorators.api_view`
  - `view` 바로 위에 `@api_view()`를 설정한다
  - `get`이 default고 다른 `HTTP_METHOD`를 허용하고 싶다면   
    List(`[]`)에 넣는다
  ```python3
  @api_view(["GET", "POST"])
  class View(~):
  ```
  - HTTP_METHOD는 if문을 `request_method`로 처리한다.
  ```python3
  if request.method == "GET":
    ...
  elif request.method == "POST":
    ...
  ```
### 5.2.1 DRF Serializer로 HTTP METHOD 처리하기
1. GET
  - `LIST형`이냐 `DETAIL형`이냐를 구분한다
  - LIST형
    ```python3
    queryset = Model.objects.all()
    serializer = Serializer(queryset, many=True)
    return Response(serializer.data)
    ```
    - queryset을 받아 serializer 처리해준뒤, `.data`하여 `Response`한다
    - queryset에 data가 여러개일 경우, `many=True`한다
  - DETAIL형
    ```python3
    from rest_framework.exceptions import NotFound
  
    try:
      queryset = Model.objects.get(pk=pk)
    except Model.DoesNotExist:
      return NotFound
    ...
    serializer = Serializer(queryset)
    return Response(serializer.data)
    ```
    - 해당 pk인 Instance가 존재하는지 확인한다.
2. POST
  ```python3
  # views.py
  serializer = Serializer(data=request.data)
  if serializer.is_valid():
    new_data = serializer.save()
    serializer = Serializer(new_data)
    return Response(serializer.data)
  else:
    return Response(serializer.errors)
  ```
  - `POST`는 client의 form data를 받아 server에서 처리하는 것이므로 `request`의 data를 `data=request.data`식으로 받는다
  - `client`가 입력한 data를 검증(`.is_valid()`)하고 검증이 성공하면 계속 진행하며, 문제가 있을 경우 `serializer.errors`를 return한다
  - 해당 data가 valid하다면 `serializer.save()`를 진행한다. POST에서 `save`는 `create`메서드에서 진행된다
  - 다시 한번 `serializer`를 진행하고 이를 `Response`해준다
  ```python3
  # serializer.py
  def create(self, validated_data):
    return Category.objects.create(
      **validated_data
    )
  ```
  - `.objects.create(~)`로 data를 DB에 생성한다
  - `valid`된 data를 `**`를 앞에 붙여 자동으로 처리하게 한다
3. PUT
  ```python3
  try:
    queryset = Model.objects.get(pk=pk)
  except Model.DoesNotExist:
    return NotFound
  ...
  serializer = Serializer(
    queryset,
    data=request.data,
    partial=True,
  )
  if serializer.is_valid():
    updated_data = serializer.save()
    serializer = Serializer(updated_data)
    return Response(serializer.data)
  else:
    return Response(serializer.errors)
  ```
  - `PUT`은 `GET`한 data를 client가 `POST`한 data로 변경하는 것이므로 `queryset`과 `request.data` 모두 필요하다
  - `partial=True`함으로써 일부 field만 입력해도 수정가능하게 한다
  - 이후 data검증(`.is_valid`)하고 `POST`와 같이 검증이 성공하면 `save`한 뒤 `Response`한다
  - PUT에서 `save`는 `update` 메서드에서 진행된다
  ```python3
  def update(self, instance, validated_data):
    instance.field1 = validated_data.get("field1_name", instance.field1)
    instance.field2 = validated_data.get("field2_name", instance.field2)
    ...
    instance.save()
    return instance
  ```
  - `instance`는 DB에 가져온 수정할 data이고   
    `validated_data`는 client가 입력할 수정될 data다
  - `instance`를 이루는 모든 `field`를 설명하고 이를 `.get`하여 수정할 data가 있으면 대체하고 아니면 기존 data로 둔다
  - 마지막으로 `instance`를 `save`하고 `return`한다
4. DELETE
  ```python3
  try:
    queryset = Model.objects.get(pk=pk)
  except Model.DoesNotExist:
    return NotFound
  ...
  from rest_framework.status import HTTP_204_NO_CONTENT

  queryset.delete()
  return Response(status=HTTP_204_NO_CONTENT)
  ```
  - 실제 DB에서 queryset을 삭제하는 과정 `.delete()`이다
  - 삭제로 인해 GET할 data가 없음을 보여주기 위해 `204 Error`를 `Response`한다.
### 5.3 DRF APIView
- FBV 대신 CBV를 사용했을 때 장점은 다음과 같다.
  - `if..elif문` 대신 `Class Method`로 `HTTP_METHOD`를 관리하여 가독성이 높다
  - `pk`인 `queryset`을 얻는 과정을 별도의 `Class Method`로 관리하면 코드가 간결해진다
- CBV를 작성하는 방법은 다음과 같다.
  1. `urls.py`에서 `class`를 view로 사용하려면 `.as_view()`을 추가해줘야 한다
    ```python3
    path("", views.RoomList.as_view()),
    ```
  2. `rest_framework.views.APIView`를 `import`하고 `inherit`한다
    ```python3
    from rest_framework.views import APIView

    class RoomList(APIView):
      ...
    ```
  3. HTTP Method 메서드의 인자는 `self`, `request` 그리고 url을 통해 받은 `변수`이다
    ```python3
    class RoomDetail(APIView):
      def get(self, request, pk):
        ...
    ```
### 5.4 DRF ModelSerializer
- 일반 Serializer가 Model Field를 일일히 대응시켜야 한다는 불편함이 있기 때문에 이를 해결해주는 게 `ModelSerializer`이다.
- `rest_framework.serializers.ModelSerializer`를 `import`한다
- `class Meta`를 열고 `model`과 `fields`를 설명한다
  ```python3
  from rest_framework import serializer
  from .models import Model


  class Serializer(ModelSerializer):
    class Meta:
      model = Model
      fields = "__all__"
  ```
  - fields는 json에 넣은 field를 튜플에 추가한다. 모든 field를 보여주려면 `"__all__"`으로 표현한다.
  - 반대로 제외할 field가 있다면 `exclude`를 한다
  - fields를 직접 입력하는 경우, `pk` 항목을 넣어주자
### 5.4.1 ModelSerializer로 `ForeignKey` 처리하기
- ForeignKey를 fields에만 언급하면 `pk`값만 나온다
- ForeignKey의 자세한 data가 필요하다면 해당 model의 `serializer`를 언급하면 된다
  ```python3
  class Serializer(ModelSerializer):

    foreign_key = FkSerializer()

    class Meta:
      model = Model
      fields = "__all__"
  ```
  - `ManytoManyField`의 경우, Serializer에 `many=True`를 언급해야 모든 개체를 포함한다
### 5.5 상황별 Serializer 만들기
1. Data 구조가 단순하고 수량이 적다면 App `Serializer` 하나면 충분하다
2. Data 개수가 많다면 `List`형과 `Detail`형을 나누어 관리한다
  - `List`형은 말그대로 목록에 드러나는 경우로 일부 정보만 드러낸다
  - `Detail`형은 특정 한 경우를 자세히 설명하는 것으로 거의 모든 정보를 드러낸다
3. `User`처럼 본인에게만 허용되는 정보가 포함된다면 `Private`, `Public`으로 나눠서 관리하며 필요할 경우 추가로 만든다
  - `Private`
  - `Public`
  - `User`의 경우, `TinyUserSerializer`를 만들어 `avatar`와 `name`만 드러낼 수 있다