import inspect
import logging

logger = logging.getLogger(__name__)


def sidekick_task(fn):
    """
    Strip back any unnecessary text so that you can grab the task name and the app
    it came from in order to create a RegisteredTask instance in the correct format

    :param: fn, Any function you want to run as a task
    :return: The original function
    """
    from sidekick.models import RegisteredTask
    try:
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
    except Exception as e:
        logger.info(f"Problem registering sidekick_task decorator: {e}")
        return fn
