from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import JobStatus
from .serializers import JobStatusSerializer


@api_view(['GET', 'POST'])
def contact_api_view(request):

    if request.method == 'GET':
        job_status = JobStatus.objects.all()
        job_status_serializer = JobStatusSerializer(job_status, many=True)
        return Response(job_status_serializer.data)

    elif request.method == 'POST':
        job_status_serializer = JobStatusSerializer(data=request.data)
        print(job_status_serializer)
        if job_status_serializer.is_valid():
            job_status_serializer.save()
            return Response(job_status_serializer.data)
        return Response(job_status_serializer.errors)



