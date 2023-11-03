from django import forms

from .models import Course


class CreateCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields =['name', 'typ','file', 'time', 'description', 'image']
       
    