from django.shortcuts import render, get_object_or_404
from .models import Profile
from course.models import Course
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Course
from .forms import CreateCourse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import JsonResponse
# Create your views here.

def list_course(request):
  profile = get_object_or_404(Student, pk=request.user.profile.id)
  all_courses = Course.objects.all()
  available_course = all_courses.exclude(profiles=profile)
  return render(request, 'profiles/list_course.html', {'profile':profile, 'available_course':available_course})


def add_course(request, course_id):
  try:
    course = Course.objects.get(pk= course_id)
    request.user.profile.courses.add(course)
    return JsonResponse({'success':True})
  except Exception as e:
    return JsonResponse({'success':False, 'error':str(e)})



@login_required
def index(request):
    print(request.user.profile.filiere)
    course_name = request.GET.get('course_name')
    courses = Course.objects.filter(typ__icontains=request.user.profile.filiere)
    list_courses = courses

    if course_name and course_name != '':
        courses = courses.filter(name__icontains=course_name)

    paginator = Paginator(courses, 3)
    page = request.GET.get('page', 1) 

    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    return render(request, 'profiles/index.html', {'courses': courses, 'list_courses': list_courses})




@login_required
def create_course(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Impossoble de créer des cours vous n\' êtes pas un professeur')
    else:
        if request.method == 'POST':
            form = CreateCourse(data=request.POST, files = request.FILES)
            if form.is_valid():
                new_course = form.save(commit=False)
                new_course.set_intervenant(request.user.username)
                new_course.save()
                return HttpResponse('Course create with success')

        else:
            form = CreateCourse()
        return render(request, "profiles/create_course.html", {'form': form})


def view_course(request, course_id):
    course_object = Course.objects.get(id=course_id)
    return render(request, "profiles/view_course.html", {'course_object': course_object })
  
  
  
