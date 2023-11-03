from django.shortcuts import render, get_object_or_404
from .models import Profile
from course.models import Course
from django.http import JsonResponse
# Create your views here.

def list_course(request):
  profiles = get_object_or_404(Profile,pk=request.user.profile.id)
  return render(request, 'profile/list_course.html', {'profiles':profiles})


def add_course(request, course_id):
  try:
    course = Course.objects.get(pk= course_id)
    request.user.profile.courses.add(course)
    return JsonResponse({'success':True})
  except Exception as e:
    return JsonResponse({'success':False, 'error':str(e)})



  
  
  
