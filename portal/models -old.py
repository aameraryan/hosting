from django.db import models


class Employee(models.Model):
    Name = models.CharField(max_length=200)

    def __str__(self):
        return self.Name


class AtMonth(models.Model):
    Name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Month'

    def __str__(self):
        return self.Name


class Attendance(models.Model):
    AtMonth = models.ForeignKey(AtMonth, on_delete=models.CASCADE, default=1, verbose_name='Month')
    AtDate = models.DateField(unique=True, verbose_name='Date')
    Full_Day = models.ManyToManyField(Employee, related_name='Full_Day', blank=True, null=True)
    Half_Day = models.ManyToManyField(Employee, related_name='Half_Day', blank=True, null=True)
    Absent = models.ManyToManyField(Employee, related_name='Absent', blank=True, null=True)

    def __str__(self):
        return str(self.AtDate)

