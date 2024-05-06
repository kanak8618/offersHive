from django.contrib import admin
from .models import *

# Register your models here.

class Product_Images(admin.TabularInline):
    model = Product_Image

class Additional_Informations(admin.TabularInline):
    model = Additional_Information

class Product_Admin(admin.ModelAdmin):
    model = Product
    inlines = (Product_Images,Additional_Informations)
    list_display = ('product_name','price','Categories','color','section')
    search_fields = ('product_name','Categories')
    list_editable = ('Categories','color','section')

class Category_Admin(admin.ModelAdmin):
    model = Category
    list_display = ('main_category','name','popular','image')
    list_editable = ['popular']

class Sub_Category_Admin(admin.ModelAdmin):
    model = Category
    list_display = ('category', 'name')
    list_editable = ['name']

class Shop_slid_Admin(admin.ModelAdmin):
    model = Shop_slid
    list_display = ('Image','label','quots','Link')
    list_editable = ['label','quots']

class Branding_Admin(admin.ModelAdmin):
    model = Branding
    list_display = ('image','title')
    list_editable = ["title"]

class Moving_text_Admin(admin.ModelAdmin):
    model = Branding
    list_display = ('name','quots','code')
    list_editable = ['quots','code']

admin.site.register(slider)
admin.site.register(banner_area)
admin.site.register(Branding,Branding_Admin)
admin.site.register(Shop_slid,Shop_slid_Admin)

admin.site.register(Main_Category)
admin.site.register(Category,Category_Admin)
admin.site.register(Sub_Category,Sub_Category_Admin)

admin.site.register(Section)
admin.site.register(Product,Product_Admin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)

admin.site.register(Brand)
admin.site.register(Moving_text,Moving_text_Admin)
admin.site.register(Color)
admin.site.register(Coupon_code)
