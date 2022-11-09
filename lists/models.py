from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
    
class List(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(default = '')
    # this only gives us the string representation of the object but we want it to be related to the list object its self
    list = models.ForeignKey(List, default= None, on_delete = models.CASCADE)

