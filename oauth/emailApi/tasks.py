from __future__ import absolute_import

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import ScheduledReport
from celery.result import AsyncResult
from django.db.models import Q
from celery.task.schedules import crontab
from celery.decorators import periodic_task



@shared_task
def send_celery_email(subject, message, email):

    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)




@periodic_task(run_every=(crontab(minute='*/1')), name="update_status_task", ignore_result=True)
def check_status():
    schedules = ScheduledReport.objects.filter(Q(status__isnull=True) | Q(status__contains='PENDING'))
    for sch in schedules:
        stat = AsyncResult(sch.task_id).status
        sch.status = stat
        sch.save()
    return 'Done'