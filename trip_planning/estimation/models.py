
from django.db import models
from Utrip.models import City


class Type(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    def __str__(self):
        return self.type


class Accommodation(models.Model):
    name = models.CharField(max_length=50)
    destination = models.ForeignKey(City, on_delete=models.CASCADE)
    type = models.ForeignKey(Type,on_delete=models.CASCADE)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.IntegerField(default=1)
    contact = models.IntegerField()
    map = models.URLField()
    img1 = models.ImageField(upload_to='pics_rooms', blank=True, null=True)
    img2 = models.ImageField(upload_to='pics_rooms', blank=True, null=True)

    def __str__(self):
        return str(self.name) if self.name else "unnammed"


class Transportation(models.Model):
    Vtype=[
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('offroader', 'Offroader'),
        ('hatchback', 'Hatchback'),
        ('crossover', 'Crossover'),
        ('hybrid', 'Hybrid'),
    ]
    origin = models.ForeignKey(City, on_delete=models.CASCADE)
    type = models.CharField(max_length=50,choices=Vtype,default='sedan')
    registeration_number = models.CharField(max_length=20)
    average_rent = models.DecimalField(max_digits=10, decimal_places=2)
    img1 = models.ImageField(upload_to='pics_vehicle', blank=True, null=True)
    img2 = models.ImageField(upload_to='pics_vehicle', blank=True, null=True)


    def __str__(self):
        return self.registeration_number
# def __str__ function is used to return exact name as entered otherwise it will return 'destination obect'


