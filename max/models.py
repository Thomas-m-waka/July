from django.db import models
from django.utils import timezone

def get_current_time():
    current_time = timezone.localtime().time()
    return str(current_time)#Guard model  



#model  for without vehicle regitsration 
class withoutvehicle(models.Model):
    name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=10)
    
    phone_number = models.CharField(max_length=15)
    company = models.CharField(max_length=100)
    purpose = models.CharField(max_length=100)
    time_in = models.TimeField(default=get_current_time)
    time_out = models.TimeField(null=True, blank=True)
    today = models.DateField(auto_now_add=True)
    idphoto = models.ImageField(null=True,blank=True,upload_to="Idphotowithoutvehicle/")  # Store the front ID picture as a base64 string
    Exit = models.BooleanField(default=False)

    def __str__(self):
        return self.name
 # model for the people with vehicle        
class withvehicle(models.Model):  
    name = models.CharField(max_length=100)      
    id_number = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    vehicle_registration = models.CharField(max_length=20)
    company = models.CharField(max_length=100)
    purpose = models.CharField(max_length=100)
    time_in = models.TimeField(default=get_current_time)
    time_out = models.TimeField(null=True)
    today = models.DateField(auto_now_add=True)
    idphoto = models.ImageField(null=True,blank=True,upload_to="IDphotowithvehicle/") 
    vehiclephoto = models.ImageField(null=True,blank=True,upload_to="Vehiclephoto/") 
    Exit = models.BooleanField(default=False)


    def __str__(self):
        return self.name   