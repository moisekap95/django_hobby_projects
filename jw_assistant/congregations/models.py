from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse # For update and create views

# Create your models here.
class Congregation(models.Model):
    
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    zip_code = models.PositiveIntegerField()
    state = models.CharField(max_length=70)
    country = models.CharField(max_length=70)
    #num_of_publisher = models.PositiveSmallIntegerField(default='')
    #num_of_student = models.PositiveSmallIntegerField(default='')
    #num_of_reg_pioneer = models.PositiveSmallIntegerField(default='')
    #num_of_aux_pioneer = models.PositiveSmallIntegerField(default='')
    #num_of_elder = models.PositiveSmallIntegerField(default='')
    #num_of_servant = models.PositiveSmallIntegerField(default='')
    phone = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    circuit_overseer = models.CharField(max_length=40, blank=True, null=True)
    circuit = models.CharField(max_length=40, blank=True, null=True)
    language = models.CharField(max_length=30, blank=True, null=True)
    #average_attendance = models.PositiveSmallIntegerField(default='')
    access_key = models.CharField(max_length=10, blank=True, null=True)
    added_by = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('congregations:detail', kwargs={'pk':self.pk}) # For update and create views
