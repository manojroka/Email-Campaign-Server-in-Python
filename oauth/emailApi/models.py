from django.db import models

# # Create your models here.

class ScheduledReport(models.Model):
   
    subject = models.CharField('Subject', max_length=200)
    message = models.CharField('Message', max_length=1000)
    email = models.EmailField('Email')
    task_id = models.CharField('Task_id', max_length=1000, null=True, blank=True)
    status = models.CharField('Status', max_length=100, null=True, blank=True)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = "scheduledReports"