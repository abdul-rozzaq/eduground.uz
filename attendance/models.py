from django.db import models

class Attendance(models.Model):
    ec = models.ForeignKey('home.EducationCenter', on_delete=models.CASCADE)
    date = models.DateField()
    group = models.ForeignKey('home.Group', on_delete=models.CASCADE)
    peoples = models.ManyToManyField('home.People', blank=True)


    def __str__(self):
        return self.date

    