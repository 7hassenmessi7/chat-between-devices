from django.db import models
from django.contrib.auth.models import User 
from django.forms import ModelForm

class Message(models.Model):

    username = models.CharField(max_length=255)
    
   
    room     = models.CharField(max_length=255)
    content  = models.TextField() 
    date_added = models.DateTimeField(auto_now_add=True)




class Meta:
    ordering = ('date_added',)



class Customer (models.Model):
    user     =  models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name     =  models.CharField(max_length=200, null=True)
    phone    =  models.CharField(max_length=200, null=True)
    email    =  models.CharField(max_length=200,null=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name



class tag (models.Model):
    name     =  models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name            



class Product(models.Model):
	CATEGORY = (
			('Indoor', 'Indoor'),
			('Out Door', 'Out Door'),
			) 

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(tag)

	def __str__(self):
		return self.name



class Order (models.Model):
    status = (
        ('pending', 'pending'),
        ('out for delivery', 'out for delivery'),
        ('Delivered','Delivered'),
        )
     
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200 ,null=True,choices=status)
    note = models.CharField(max_length=500 ,null=True)

    def __str__(self):
   		return self.product.name



class Files(models.Model):
    filename = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='store/pdfs/')
    cover = models.ImageField(upload_to='store/covers/', null=True, blank=True)

    def __str__(self):
        return self.filename

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)







class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='store/pdfs/')
    cover = models.ImageField(upload_to='store/covers/', null=True, blank=True)

    def __str__(self):
        return self.title


    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)


