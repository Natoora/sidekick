from django.contrib import admin
from sidekick.models import Task, CronSchedule
from import_export import resources


class CronScheduleResource(resources.ModelResource):
    """
    CronSchedule Resource for import_export
    """
    class Meta:
        model = CronSchedule


class CronScheduleAdmin(admin.ModelAdmin):
    """
    Admin for the CronSchedule
    """

    model = CronSchedule
    fields = (
        'name',
        'minute',
        'hour',
        'day_of_week',
        'day_of_month',
        'month_of_year'
    )


admin.site.register(CronSchedule, CronScheduleAdmin)


class TaskResource(resources.ModelResource):
    """
    Task Resource for import_export
    """
    class Meta:
        model = Task


class TaskAdmin(admin.ModelAdmin):
    """
    Admin for the task model
    """

    list_display = ['name', 'registered_task', 'status', 'running_for', 'cron_schedule', 'enabled']


admin.site.register(Task, TaskAdmin)
