from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from .tasks import send_celery_email, check_status

from .serializers import ScheduleSerializer
from .models import ScheduledReport
from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult

def index(request):
    add = send_celery_email.delay('hello', 'welcome to my world', '72bct601@wrc.edu.np')
    print(add)
    return HttpResponse('Task done!!')


@api_view(["GET"])
@csrf_exempt 
def welcome(request):

    schedules = ScheduledReport.objects.filter(Q(status__isnull=True) | Q(status__contains='PENDING'))
    # print(schedules)
    for sch in schedules:
        stat = AsyncResult(sch.task_id).status
        sch.status = stat
        sch.save()
    return JsonResponse({'result': 'Work Done'}, status = status.HTTP_200_OK)



@api_view(["GET", "POST"])
@csrf_exempt
def schedules(request):
    if request.method == 'GET':
   
        schedules = ScheduledReport.objects.all()
        # print(schedules)
        serializer = ScheduleSerializer(schedules, many=True)
        return JsonResponse({'schedules': serializer.data}, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def check(id):
    result = AsyncResult(id).ready()
    return result





@api_view(["GET"])
@csrf_exempt
def run_schedules(request):
    schedules = ScheduledReport.objects.all()
    
    for sch in schedules:
        if sch.task_id is None:
            scheduled = send_celery_email.delay(subject=sch.subject, message=sch.message, email=sch.email)
            print(scheduled.task_id)
            print(scheduled.status)
            sch.task_id = scheduled.task_id
            sch.status = scheduled.status
            sch.save()
        else:
            
            result = check(sch.task_id)

          
            if result:
                print(result)
                return JsonResponse({'result': 'Work Done'}, status = status.HTTP_200_OK)
               
            else:
               
                scheduled = send_celery_email.delay(subject=sch.subject, message=sch.message, email=sch.email)
                print(scheduled.task_id)
                print(scheduled.status)
                sch.task_id = scheduled.task_id
                sch.status = scheduled.status
                sch.save()
     
    return JsonResponse({'result': 'Work Done'}, status = status.HTTP_200_OK)
    
   

@api_view(["GET"])
@csrf_exempt
def check_schedule(request):
    check_status().delay()
    return JsonResponse({'result': 'Status Updated'}, status = status.HTTP_200_OK)




def home(request):
    return HttpResponse('Welcome home!!')