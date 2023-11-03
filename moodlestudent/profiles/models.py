from django.db import models
from django.conf import settings
from course.models import Course
# Create your models here.
class Profile(models.Model):
    COMPUTER_SCIENCE='Computer Science'
    A2I='A2I'
    MECHANICAL='Mechanical'
    GI = 'GI'
    CHOICE_TYPE_OF_COURSE=[
        (COMPUTER_SCIENCE, "Computer Science"),
        (A2I, "A2I"),
        (MECHANICAL, "Mechanical"),
        (GI, "GI")
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    image = models.ImageField(max_length=255, default=None, upload_to='images/users/%Y/%m/%d', blank=True)
    filiere = models.CharField(max_length=20, default= COMPUTER_SCIENCE,choices =CHOICE_TYPE_OF_COURSE) 
    courses = models.ManyToManyField(Course)
    
