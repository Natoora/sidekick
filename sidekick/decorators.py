import inspect
import logging

from django.db import connection

logger = logging.getLogger(__name__)

try:
    # This is here in case you have tasks decorated before running migrations
    # It will just return the original function if the table does not exist
    db_ready = 'sidekick_registeredtask' in connection.introspection.table_names()
except Exception as e:
    logger.info(f"DB not ready when registering SideKick task: {e}")
    db_ready = False

if db_ready:
    def sidekick_task(fn):
        """
            Strip back any unnecessary text so that you can grab the task name and the app
            it came from in order to create a RegisteredTask instance in the correct format
            :param fn: Any function you want to run as a task
            :return: The original function
            """
        from sidekick.models import RegisteredTask

        src = inspect.getsource(fn)
        module_name = inspect.getmodule(fn).__name__.split('.')[0]
        task_string = src.split('(')[0][17:].replace('f ', '{} --'.format(module_name))
        try:
            RegisteredTask.objects.get(task_name=task_string)
        except RegisteredTask.DoesNotExist:
            st = RegisteredTask()
            st.task_name = task_string
            st.save()
        return fn
else:
    def sidekick_task(fn):
        return fn
