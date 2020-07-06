import logging

from django.conf import settings

from sidekick.models import Task
from sidekick.services.helpers import update_task_status


logger = logging.getLogger(__name__)


class CronService:
    """Service to create or re-write the cron files """

    def __init__(self):
        if all([getattr(settings, "SIDEKICK")['SIDEKICK_REGISTERED_APPS'],
                getattr(settings, "SIDEKICK")['MANAGE_PATH'],
                getattr(settings, "SIDEKICK")['CRON_PATH']]):
            self.manage_path = settings.SIDEKICK['MANAGE_PATH']
        else:
            logger.error(
                msg="Missing one of SIDEKICK_REGISTERED_APPS, MANAGE_PATH or CRON_PATH in settings file."
            )

    def write_cron_file(self, tasks):
        """For each task in list, write to the cron file. """

        with open(settings.SIDEKICK['CRON_PATH'], 'w+') as ws_cron_file:
            logger.info('Cron file opened at: ', settings.SIDEKICK['CRON_PATH'])
            for task in tasks:
                logger.info('Writing task to file: ', task.name)
                ws_cron_file.write(
                    "# {name}\n"
                    "{schedule} {manage_path} {task}\n\n".format(
                        name=task.name,
                        schedule=task.cron_schedule.schedule(),
                        manage_path=self.manage_path,
                        task=task.registered_task.task_name)
                )

    def generate_cron_tasks(self):
        """Create a new cron file on the post save of a Registered Task"""
        try:
            tasks = Task.objects.filter(enabled=True)
            self.write_cron_file(tasks=tasks)
            sleeping_tasks = Task.objects.filter(enabled=False)
            for st in sleeping_tasks:
                update_task_status(registered_task_name=st.registered_task.task_name, status=Task.SLEEPING)
            logger.info(msg='Cron tasks successfully created.')
        except Exception as e:
            logger.error(msg='Failed to write cron tasks due to {}'.format(e))
