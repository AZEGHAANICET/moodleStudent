from django.db import models
import os 
from django.core.exceptions import ValidationError
from datetime import datetime
from PIL import Image
# Create your models here.
class Course(models.Model):
    AUTOMNE='Automne'
    PRINTEMPS='Printemps'
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
    CHOICES_TIME = [(AUTOMNE, 'Automne'),
    (PRINTEMPS, 'Printemps'),]
    def get_file_upload_path(instance, filename):
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        return os.path.join("images/Files", current_time, instance.typ, filename)
    def get_image_upload_path(instance, filename):
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        return os.path.join("images/courses", current_time, instance.typ, filename)

    name = models.CharField(max_length=200)
    typ = models.CharField(max_length =20, choices=CHOICE_TYPE_OF_COURSE, default=COMPUTER_SCIENCE)
    intervenant = models.CharField(max_length=200, default=None)
    creation_date = models.DateField(auto_now_add=True)
    file = models.FileField(max_length=200, upload_to=get_file_upload_path)
    time = models.CharField(max_length=10, choices =CHOICES_TIME, default=AUTOMNE)
    description = models.TextField(default=None)
    image = models.ImageField(default=None, blank=True, upload_to=get_image_upload_path)


    def deux_premieres_phrases(self):
        phrases = self.description.split('.')
        deux_premieres_phrases = '.'.join(phrases[:2])
        return deux_premieres_phrases

    def set_intervenant(self, value):
        self.intervenant = value
    def __str__(self):
        return self.name
    def clean(self):
        print("clean pro")
        super().clean()
        if self.file:
            max_size = 10 * 1024 * 1024
            if self.file.size > max_size:
                raise ValidationError("La taille du fichier ne doit pas dépasser 10 Mo.")
 
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        new_size = (300, 200) 
        img.thumbnail(new_size)
        img.save(self.image.path)