from django.urls import path, include
from . import views
app_name="profiles"
urlpatterns = [
    path('', views.list_course, name='index'),
    path('view_course/', views.view_course, name='view_course'),
    path('add/<int:course_id>', views.add_course, name='add_course'),
]
