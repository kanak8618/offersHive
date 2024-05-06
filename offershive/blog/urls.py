from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('blog',views.BLOG, name='blog'),
    path('blog/<slug:slug>',views.BLOG_DETAIL, name='blog_detail'),

] +static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
