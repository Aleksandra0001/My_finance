# My Finance App #
### Web-application of personal finance accounting with Django and Tailwind CSS. ###
### The application allows you to save all income and expenses in several categories and to report total income/expenditure for a specified period of time. ###

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Aleksandra0001/Python_web/tree/main/Homework_13_Django_tailwind/my_finance
$ cd my_finance
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Then we need to install django-tailwind:

```sh
(env)$ pip install django-tailwind
```

Add 'tailwind' to INSTALLED_APPS in settings.py:

```sh
INSTALLED_APPS = [
    ...
    'tailwind',
]
```

Create a Tailwind CSS compatible Django app, I like to call it theme:

```sh
python manage.py tailwind init
```

Add your newly created 'theme' app to INSTALLED_APPS in settings.py:

```sh
INSTALLED_APPS = [
  'tailwind',
  'theme'
]
```

Register the generated 'theme' app by adding the following line to settings.py file:

```sh
TAILWIND_APP_NAME = 'theme'
```

Make sure that the INTERNAL_IPS list is present in the settings.py file and contains the 127.0.0.1 ip address:

```sh
INTERNAL_IPS = [
    "127.0.0.1",
]
```

Install Tailwind CSS dependencies, by running the following command:

```sh
python manage.py tailwind install
```

Let’s also add and configure django_browser_reload, which takes care of automatic page and css refreshes in the development mode. Add it to INSTALLED_APPS in settings.py:

```sh
INSTALLED_APPS = [
  # other Django apps
  'tailwind',
  'theme',
  'django_browser_reload'
]
```

Staying in settings.py, add the middleware:

```sh
MIDDLEWARE = [
  # ...
  "django_browser_reload.middleware.BrowserReloadMiddleware",
  # ...
]
```
The middleware should be listed after any that encode the response, such as Django’s GZipMiddleware. The middleware automatically inserts the required script tag on HTML responses before </body> when DEBUG is True.

Include django_browser_reload URL in your root url.py:

```sh
from django.urls import include, path
urlpatterns = [
    ...,
    path("__reload__/", include("django_browser_reload.urls")),
]
```

Finally, you should be able to use Tailwind CSS classes in HTML. Start the development server by running the following command in your terminal:

```sh
python manage.py tailwind start
```


Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd project
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/.
