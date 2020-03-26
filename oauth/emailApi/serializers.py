from rest_framework import serializers

from .models import ScheduledReport

class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScheduledReport
        fields = ['id', 'subject', 'message', 'email', 'status', 'task_id']