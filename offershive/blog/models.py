from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from django.utils.html import format_html
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True, null=True)
    image = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title

class InstaFeed(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Post(models.Model):
    blog_title = models.CharField(max_length=100)
    Tags = models.CharField(max_length=50,null=True)
    image = models.ImageField(upload_to='media/blog/post', null=True)
    Description = RichTextField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    quots = models.TextField(max_length=1000, null=True, blank=True)
    popular = models.BooleanField(default=False)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    instafeed = models.ForeignKey(InstaFeed, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(default='', max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.blog_title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("blog_detail", kwargs={'slug': self.slug})  # blog_detail - name of blog_detail url

    class Meta:
        db_table = "blog_Post"  # app -blog   model -Post

def create_slug(instance, new_slug=None):
    slug = slugify(instance.blog_title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Post)