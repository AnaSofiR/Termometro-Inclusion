from django.db import models
from analitica.models import *
from django.db.models import Avg

# Create your models here.        

class Recomendation(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    description = models.TextField(blank=False, null=False)   


class Discrimination(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    type = models.CharField(max_length=45, blank=False, null=False, default="Sin discriminación")
    recomendation = models.ForeignKey(Recomendation, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.type


class Offer(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    education_level = models.CharField(blank=False, null=False, max_length=45)
    salary = models.FloatField(blank=False, null=False)
    city = models.CharField(blank=False, null=False, max_length=45)
    discrimination = models.ManyToManyField(Discrimination)
    state = models.BooleanField(default=False)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True)

    def average_rating(self) -> float:
        return Rating.objects.filter(offer=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return f"{self.title}: {self.average_rating()}"

    

class Rating(models.Model):
    candidate = models.ForeignKey(Candidates, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)  

    def __str__(self):
        return f"{self.offer.title}: {self.rating}"     

    
 
class NewOffer(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    description = models.TextField(blank=False, null=False)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)





