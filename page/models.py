from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE,blank=True)
    name = models.CharField(max_length=200,null=True)
    Phone = models.CharField(max_length=200,null=True) 
    email1 = models.CharField(max_length=200,null=True)
    profile_pic=models.ImageField(default='user.jpg',null=True,blank=True)
    date_cretaed= models.DateTimeField(auto_now_add=True,null=True)


    def __str__(self):
        return self.name
    

    
class Product(models.Model):
    CATEGORY=(
        ('Indoor','Indoor'),
        ('Out Door','Out Door')
    )


    name=models.CharField(max_length=200,null=True)
    price=models.CharField(max_length=200,null=True)
    category=models.CharField(max_length=200,null=True,choices=CATEGORY)
    description=models.CharField(max_length=200,null=True)
    date_cretaed= models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return str(self.name)
    tag=models.ManyToManyField(Tag)




class Order(models.Model):
    STATUS=(('Pending','Pending'),
            ('Out for delivery','Out for delivery'),
            ('Delivered','Delivered')
            )


    customer= models.ForeignKey(Customer,null= True, on_delete=models.SET_NULL)
    product= models.ForeignKey(Product,null= True, on_delete=models.SET_NULL)
    name=models.CharField(max_length=200,null=True, choices=STATUS)
    date_created= models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name



    
