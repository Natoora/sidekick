import importlib
import logging

from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)


class SidekickConfig(AppConfig):
    name = 'sidekick'

    def ready(self):
        self.register_tasks()

    @staticmethod
    def register_tasks():
        """
        For each app listed in SIDEKICK_REGISTERED_APPS import the task to trigger the decorator
        """
        try:
            for app in settings.SIDEKICK['SIDEKICK_REGISTERED_APPS']:
                app_task_path = f"{app}.tasks"
                try:
                    importlib.import_module(app_task_path)
                except ModuleNotFoundError:
                    pass
                except Exception as e:
                    logger.exception(f"Failed to import app task exception=({e})")
        except Exception as e:
            logger.exception(f"Failed to register tasks for Side Kick exception=({e})")
