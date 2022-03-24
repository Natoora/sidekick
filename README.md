# Sidekick

Sidekick is a simple scheduler for Django management commands.  Simply create the task, add the decorator and then 
set when it should run from Django's admin. 

![Side Kick Admin Example](./sidekick/static/images/SideKickAdmin.png?raw=true "Side Kick Admin Example")


---

## Development

#### Install requirements
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Management
Use the `manage.py` file as you would in a normal Django project.  
It has been configured with the basic settings to make migrations and run tests.
```shell
python manage.py makemigrations
python manage.py test
```

---

## Usage

#### Install
```shell
pip install git+https://github.com/Natoora/sidekick.git
```

#### Add to installed apps
```python
INSTALLED_APPS = [
    ...,
    sidekick
]
```

#### Add Sidekick settings

```python
from django.conf import settings

SIDEKICK = {
    "SIDEKICK_REGISTERED_APPS": settings.CUSTOM_APPS_LIST,  # List of apps to search for tasks in
    "MANAGE_PATH": "/code/manage.py",  # Path to manage.py from base dir
    "CRON_PATH": "/var/spool/cron/crontabs/root",  # Path for Cron file 
    "LOCK_PATH": "/sidekick/lock_files/",  # Path to store lock files 
}
```

#### Run migrations
```shell
./manage.py migrate
```

#### Register Tasks
Functions must be in a `tasks.py` file in the root of a registered app with the `@sidekick_task` decorator.
```python
# app/tasks.py

from sidekick.decorators import sidekick_task

@sidekick_task
def my_new_task():
    ...
```

#### Setup management command

Create a new directory within the app called ``management`` and then a subdirectory called `commands`. Add a
``__init__.py`` file and then a file with the name of the app eg. ``customers.py`` to the ``commands`` directory.

If you already have management commands in this file, that is fine, you can skip this step, but make sure to add the 
code for ``add_arguments()`` and also ``handle()`` in the next step.

File structure would be as follows:

    myproject
    |_ customers
       |_management
         |_commands
            |_ __init__.py
            |_ customers.py

Within ``customers.py`` (or whatever your app is) add the following:

```python
import logging

from django.core.management.base import BaseCommand
from sidekick.services.helpers import get_task_name, get_app_name
from sidekick.services.crontab import CronTask

from sidekick.models import RegisteredTask

logger = logging.getLogger(__name__)
app_name = get_app_name(__name__)


class Command(BaseCommand):
    help = "Commands for the Stock app"

    def add_arguments(self, parser):
        """Defines the arguments """

        for task in RegisteredTask.objects.filter(task_name__startswith=app_name):
            task_name = task.task_name.split(' ')[1]
            parser.add_argument(
                task_name,
                action='store_true',
                dest=task_name[2:]
            )

    def handle(self, *args, **options):
        """Handle stock management commands.

        :param args:
        :param options: Arguments passed with command e.g. send_emails_to_customers, verbosity etc.
        """
        task_name = get_task_name(options)
        rt_task_name = "{} --{}".format(app_name, task_name)

        if RegisteredTask.objects.filter(task_name=rt_task_name):
            try:
                CronTask(task_name=task_name, registered_task_name=rt_task_name, app=app_name).run()
            except Exception as e:
                logger.error(msg=e)
```

You will need to have this same file structure in each app you want to have tasks registered to.
