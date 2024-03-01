from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price','quantity','description']

admin.site.register(Cart)

class OrderDetailsInline(admin.TabularInline):
    model = OrderDetail
    extra = 0
    readonly_fields =('product','quantity','unit_price','total_price')
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDetailsInline]
    readonly_fields = ('name','total_order_price','user')
    list_display =['name','total_order_price','status']
    
admin.site.register(WishList)
    