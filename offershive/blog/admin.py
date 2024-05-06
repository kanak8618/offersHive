from django.contrib import admin
from .models import *

# Register your models here.

class Ctg_Admin(admin.ModelAdmin):
    model = Category
    list_display = ('title','date')

class Post_Admin(admin.ModelAdmin):
    model = Post

    def image_tag(self, obj):
        return format_html('<img src="{}" style="height:50px; width:50px; border-radius:10px" />'.format(obj.image.url))

    list_display = ('image_tag','Tags','blog_title','popular','Category','date')
    search_fields = ('blog_title','Category')
    list_editable = ('popular','Category')


admin.site.register(Category,Ctg_Admin)
admin.site.register(InstaFeed)
admin.site.register(Post,Post_Admin)