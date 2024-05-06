from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from .models import Category, InstaFeed, Post
# from .shop.models import Main_Category


# Create your views here.

def BLOG(request):
    # main_category = Main_Category.objects.all().order_by('-id')
    post = Post.objects.all()
    popular = Post.objects.filter(popular = True).order_by('id')[0:6]
    category = Category.objects.all()
    insta_feed = InstaFeed.objects.all()

    paginator = Paginator(post, 8)
    page_no = request.GET.get('page')
    post = paginator.get_page(page_no)

    context = {
        # 'main_category':main_category,
        'post':post,
        'popular':popular,
        'category':category,
        'insta_feed':insta_feed,
    }
    return render(request, 'blog/blog.html',context)

def BLOG_DETAIL(request,slug):
    # main_category = Main_Category.objects.all().order_by('-id')
    popular = Post.objects.filter(popular=True).order_by('id')
    post = Post.objects.filter(slug = slug)

    if post.exists():
        post = Post.objects.filter(slug = slug)
    else:
        return redirect('not_found404')

    context = {
        'post':post,
        # 'main_category':main_category,
        'popular':popular,
    }
    return render(request, 'blog/blog_detail.html',context)