from django.urls import path, include
from . import views
app_name="course"
urlpatterns = [
    path('', views.index, name='index'),
    path('create_course/', views.create_course, name='create_course'),
    path('<int:course_id>', views.view_course, name='view_course'),
]
