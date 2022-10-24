## Poetry-Django Template on GitPod

Initialize Django Project which runs on fine-tuned python virtual environment, [`Poetry`](https://python-poetry.org/).   
Poetry has excellent feature on not only Dependencies Management but also exclusively provide `dependencies lock`, `packages batch install&update` which is not provided from other python venvs.

Modification added in [`.gitpod.yml`](./.gitpod.yml) which automatically set venv on project, install django, start django project, set port on localhost for development, solve csrf-problem and quick admin panel configuration.   
To learn more, please see the [Getting Started](https://www.gitpod.io/docs/getting-started) documentation.   

## How to configurate Django Project Manually
If you are working in local environment, so you have to configure project manually.
These are the step you have to follow to create exact result like this:
1. Install Python 3.8^
  - Django 4.0 requirements is >= python 3.8
  - Lower python version could cause installation problem with django
2. Configure Poetry
  - Install Poetry
  ```shell
  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  ```
  - Start Poetry on Project
  ```shell
  poetry init -n
  ```
3. Add Django with Poetry and Start Django Project
  - Install Django with Poetry
  ```shell
  poetry add django
  ```
  - Start Django Project
  ```shell
  poetry run django-admin startproject config .
  ```
4. Set or Overwrite [`config.settings`](./config/settings.py) to operate server successfully
  ```python3
  ALLOWED_HOSTS = ["localhost"]
  CSRF_TRUSTED_ORIGINS = ["https://*.ws-us72.gitpod.io"]

  TIME_ZONE = 'Asia/Seoul'
  ```
5. Preparation to access Admin Panel
  - Create Admin Account
  ```shell
  poetry run python manage.py migrate
  poetry run python manage.py createsuperuser
  poetry run python manage.py runserver
  ```
  - redirect to `/admin` and log-in on Admin
  - Admin Panel successfully opened then finish!

## PostScript📝
- Dedicated to [`@cosmos1030`](https://github.com/cosmos1030) who introduce gitpod and implemented template with django
- Feel free to use this template and any feedback by issue or discussion is welcome.😉
- 📬Contact: `akang8150@naver.com`📬