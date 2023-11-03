from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Course
from .forms import CreateCourse
from django.core.paginator import Paginator, EmptyPage,  PageNotAnInteger

# Create your views here.

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

    return render(request, 'course/index.html', {'courses': courses, 'list_courses': list_courses})




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
        return render(request, "course/create_course.html", {'form': form})


def view_course(request, course_id):
    course_object = Course.objects.get(id=course_id)
    return render(request, "course/view_course.html", {'course_object': course_object })