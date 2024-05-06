from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import *
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min, Sum
from cart.cart import Cart
from django.core.paginator import Paginator

def HOME(request):
    sliders = slider.objects.all().order_by('-id')[0:3]
    banners = banner_area.objects.all().order_by('-id')[0:3]
    main_category = Main_Category.objects.all().order_by('-id')
    product = Product.objects.filter(section__name = "Top Deals Of The Day")
    product2 = Product.objects.filter(section__name = "Recommended For You")
    product3 = Product.objects.filter(section__name = "Hot Trending Products")
    product4 = Product.objects.filter(section__name = "On-sale Products")
    product5 = Product.objects.filter(section__name = "Top Rate Products")
    branding = Branding.objects.all()
    category = Category.objects.filter(popular = True)
    moving_text = Moving_text.objects.all()

    context = {
        'sliders':sliders,
        'banners':banners,
        'main_category':main_category,
        'product':product,
        'product2':product2,
        'product3':product3,
        'product4':product4,
        'product5':product5,
        'branding':branding,
        'category':category,
        'moving_text':moving_text,
    }
    return render(request,'main/index.html',context)

def PRODUCT_DETAIL(request, slug):
    main_category = Main_Category.objects.all().order_by('-id')
    product = Product.objects.filter(slug = slug)
    if product.exists():
        product = Product.objects.get(slug=slug)
    else:
        return redirect('not_found404')

    cotext = {
        'product':product,
        'main_category':main_category,
    }
    return render(request,'product/product_detail.html',cotext)

def NOT_FOUND404(request):
    return render(request, 'error/404.html')

def SIGNIN(request):
    return render(request, 'registration/register.html')
def REGISTER(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():       # check username already register or not
            messages.error(request, 'Username already exists')
            return redirect('login')

        if User.objects.filter(email=email).exists():             # check email already register or not
            messages.error(request, 'Email ID already exists')
            return redirect('login')

        user = User(
            username = username,
            email = email,
        )
        user.set_password(password)
        user.save()
        return redirect('login')

def LOGIN(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username and Password are invalid')
            return redirect('login')
@login_required(login_url='/accounts/login/')
def PROFILE(request):
    return render(request,'registration/profile.html')

@login_required(login_url='/accounts/login/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)         #if here id is ge then update old data with new data otherwise add new data

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":   # if user want to update password, it will be set new password other wise directly save other new info..
            user.set_password(password)

        user.save()
        messages.success(request, 'Profile Are Successfully Updated. ')
        return redirect('profile')

def ABOUT_US(request):
    main_category = Main_Category.objects.all().order_by('-id')
    context = {
        'main_category':main_category,
    }
    return render(request, 'main/about_us.html',context)

def CONTACT_US(request):
    main_category = Main_Category.objects.all().order_by('-id')
    context = {
        'main_category': main_category,
    }
    return render(request, 'main/contact_us.html',context)

def FAQS(request):
    main_category = Main_Category.objects.all().order_by('-id')
    context = {
        'main_category': main_category,
    }
    return render(request, 'main/faqs.html',context)

def SHOP(request):
    main_category = Main_Category.objects.all().order_by('-id')
    shop_slide = Shop_slid.objects.all().order_by('-id')
    category = Category.objects.all()
    product = Product.objects.all()
    color = Color.objects.all()
    ColorID = request.GET.get('colorID')
    brand = Brand.objects.all()
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    FilterPrice = request.GET.get('FilterPrice')

    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte=Int_FilterPrice)
    elif ColorID:
        product = Product.objects.filter(color=ColorID)
    else:
        product = Product.objects.all()


    paginator = Paginator(product, 12)
    page_no = request.GET.get('page')
    product = paginator.get_page(page_no)

    context = {
        'shop_slide':shop_slide,
        'main_category':main_category,
        'category':category,
        'product':product,
        'min_price':min_price,
        'max_price':max_price,
        'FilterPrice':FilterPrice,
        'color':color,
        'brand':brand,
    }
    return render(request, 'main/shop.html',context)

def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    product_num = request.GET.getlist('product_num[]')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()

    if len(product_num) > 0:
        allProducts = allProducts.all().order_by('-id')[0:1]

    t = render_to_string('ajax/product.html', {'product': allProducts})
    return JsonResponse({'data': t})

def filter_product(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    product_num = request.GET.getlist('product_num[]')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()

    if len(product_num) > 0:
        allProducts = allProducts.all().order_by('-id')[0:1]

    t = render_to_string('ajax/product2.html', {'product': allProducts})
    return JsonResponse({'data': t})
@login_required(login_url='/accounts/login/')
def cart_add(request,id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect('cart_detail')

@login_required(login_url='/accounts/login/')
def item_clear(request,id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect('cart_detail')

@login_required(login_url='/accounts/login/')
def item_increment(request,id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect('cart_detail')

@login_required(login_url='/accounts/login/')
def item_decrement(request,id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect('cart_detail')

@login_required(login_url='/accounts/login/')
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

@login_required(login_url='/accounts/login/')
def cart_detail(request):
    main_category = Main_Category.objects.all().order_by('-id')
    cart = request.session.get('cart')
    Packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)

    context = {
        'packing_cost':Packing_cost,
        'tax':tax,
        'main_category':main_category,
    }
    return render(request,'main/cart.html',context)

@login_required(login_url='/accounts/login/')
def CHECKOUT(request):
    main_category = Main_Category.objects.all().order_by('-id')

    cart = request.session.get('cart')
    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)

    valid_coupon = None
    coupon_code = None
    coupon = None
    invalid_coupon = None
    if request.method == 'GET':
        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon_code.objects.get(code=coupon_code)
                valid_coupon = 'Are Applicable On Current Order !'
            except:
                invalid_coupon = 'invalid Coupon Code !'

    context = {
        'packing_cost': packing_cost,
        'main_category': main_category,
        'tax': tax,
        'coupon': coupon,
        'coupon_code': coupon_code,
        'valid_coupon': valid_coupon,
        'invalid_coupon': invalid_coupon,
    }
    return render(request, 'main/checkout.html',context)

def MY_ORDER(request):
    main_category = Main_Category.objects.all().order_by('-id')
    context = {
        'main_category':main_category,
    }
    return render(request, 'main/my-order.html',context)

def BLOG(request):
    main_category = Main_Category.objects.all().order_by('-id')
    context = {
        'main_category':main_category,
    }
    return render(request, 'blog/blog.html',context)

def TRACK_ORDER(request):
    main_category = Main_Category.objects.all().order_by('-id')
    context = {
        'main_category':main_category,
    }
    return render(request, 'main/track-order.html',context)