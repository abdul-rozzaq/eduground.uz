from django.db import models
from django.contrib.auth.models import User

from datetime import timedelta

class EducationCenter(models.Model):
    logo = models.ImageField(upload_to='logo/')
    name = models.CharField(max_length=256)
    password = models.CharField(max_length=128)    
    admins = models.ManyToManyField(User)
    
    def __str__(self) -> str:
        return self.name

class Day(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class People(models.Model):
    ec = models.ForeignKey(EducationCenter, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=256)
    phone = models.CharField(max_length=15)
    birthday = models.DateField()
    balans = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name

class Teacher(models.Model):
    ec = models.ForeignKey(EducationCenter, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=256)
    phone = models.CharField(max_length=15)
    birthday = models.DateField()

    def __str__(self):
        return self.full_name


class Course(models.Model):
    ec = models.ForeignKey(EducationCenter, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    duration = models.IntegerField(default=2)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Group(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    peoples = models.ManyToManyField(People, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.ManyToManyField(Day)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Lid(models.Model):
    ec = models.ForeignKey(EducationCenter, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=256)
    phone = models.CharField(max_length=15)
    data = models.TextField(max_length=1000)

    def __str__(self):
        return self.full_name

