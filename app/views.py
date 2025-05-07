from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from app.models import SellerDetail
from django.contrib.auth.decorators import login_required
from product.models import Product
from app.models import SellerDetail

# Create your views here.

@login_required
def home(request):
    user = request.user
    seller_details = SellerDetail.objects.filter(user=user).first()
    products = Product.objects.all().order_by('-created_at')
    my_products = products.filter(seller=user)
    market_place = products.exclude(seller=user)
    context = {'market_place': market_place, 'my_products': my_products, "seller_details":seller_details}
    return render(request, 'app/home.html', context)

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        user_type = request.POST.get("user_type")
        
        phone = request.POST.get("phone")
        brand = request.POST.get("brand")
        address = request.POST.get("address")
        bank = request.POST.get("bank")
        account_number = request.POST.get("account_number")
        if not username or not user_type or not email or not password or not cpassword:
            messages.error(request, 'All fields are required')
            return redirect(signup)
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect(signup)
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken')
            return redirect(signup)
        if len(password) < 8 :
            messages.error(request, 'Password too short')
            return redirect(signup)
        if password != cpassword :
            messages.error(request, 'Password did not match')
            return redirect(signup)
        if user_type == "SELLER":
            if not phone or not brand or not bank or not account_number or not address:
                messages.error(request, 'All seller info are required')
                return redirect(signup)
        user = User.objects.create(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        if user_type == "SELLER":
            SellerDetail.objects.create(
                user=user,
                address=address,
                brand_name=brand,
                phone=phone,
                bank_name=bank,
                account_number=account_number
            )

        messages.success(request, 'Account crerated successfully')
        return redirect(login)
    return render(request, 'app/signup.html')



def login(request):
    next_url = request.GET.get('next')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            messages.error(request, 'All fields are required')
            return redirect(signup)
        
        user = auth.authenticate(username=username, password=password)
        if not user:
            messages.error(request, 'Invalid login credentials')
            return redirect(signup)
        auth.login(request, user)
        messages.success(request, 'Login successful')
        return redirect(next_url or home)
    return render(request, 'app/login.html')

def logout(request):
    auth.logout(request)
    return redirect(login)