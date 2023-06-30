from django.contrib import admin
from .models import *

admin.site.register(Message)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(tag)
admin.site.register(Order)

admin.site.register(Files)
