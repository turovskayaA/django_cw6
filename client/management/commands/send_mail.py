from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from client.services.send_mail import send_mails


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Run APScheduler"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), alias="default")

        scheduler.add_job(
            send_mails,
            trigger=CronTrigger(second="*/30"),
            id="sendmail",
            max_instances=10,
            replace_existing=True,
        )

        try:
            print("Start scheduler")
            scheduler.start()
        except KeyboardInterrupt:
            print("Stop scheduler")
            scheduler.shutdown()
            print("Successful")

