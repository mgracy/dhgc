from django.contrib import admin
from .models import Emp, Role, Customer, Supplier, Cash_Credit_Limit
# Register your models here.
admin.site.register(Emp)
admin.site.register(Role)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Cash_Credit_Limit)