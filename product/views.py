from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Product
from app.models import SellerDetail

# Create your views here.
@login_required
def add_product(request):
    user = request.user
    seller_details = SellerDetail.objects.filter(user=user).first()
    if not seller_details:
        messages.error(request, "UNAUTHORIZED")
        return redirect("/")
    if request.method == 'POST':
        user = request.user
        name= request.POST.get('name')
        quantity= request.POST.get('quantity')
        price= request.POST.get('price')
        description= request.POST.get('description')
        picture= request.FILES.get('picture')
        if not name or not quantity or not price or not picture:
            messages.error(request, 'Please provide all fields')
            return redirect(add_product)
        try:
            quantity = int(quantity)
            price = int(price)
        except:
            messages.error(request, 'Price and quantity must be numbers')
            return redirect(add_product)
        if quantity < 1 or price < 1:
            messages.error(request, 'Price and quantity must be positive numbers')
            return redirect(add_product)

        Product.objects.create(
            name=name,
            quantity=quantity,
            price=price,
            description=description,
            picture = picture,
            seller = user
        )
        messages.success(request, 'Product added successfully')
        return redirect('/')

    return render(request, 'product/add_product.html')

@login_required
def edit_product(request, id):
    user = request.user
    seller_details = SellerDetail.objects.filter(user=user).first()
    if not seller_details:
        messages.error(request, "UNAUTHORIZED")
        return redirect("/")
    product = Product.objects.filter(id=id, seller = user).first()
    if not product:
        return redirect("/")
    
    if request.method == "POST":
        name= request.POST.get('name')
        quantity= request.POST.get('quantity')
        price= request.POST.get('price')
        description= request.POST.get('description')
        picture= request.FILES.get('picture')
        if not name or not quantity or not price:
            messages.error(request, 'Please provide all fields')
            return redirect(add_product)
        try:
            quantity = int(quantity)
            price = int(price)
        except:
            messages.error(request, 'Price and quantity must be numbers')
            return redirect(add_product)
        if quantity < 1 or price < 1:
            messages.error(request, 'Price and quantity must be positive numbers')
            return redirect(add_product)
        product.name = name
        product.quantity = quantity
        product.price = price
        product.description = description or product.description
        product.picture = picture or product.picture
        product.save()
        messages.success(request, "Product updated successfully")
        return redirect("/")
    context = {'product': product}
    return render(request, "product/edit_product.html", context)

@login_required
def delete_product(request, id):
    user = request.user
    seller_details = SellerDetail.objects.filter(user=user).first()
    if not seller_details:
        messages.error(request, "UNAUTHORIZED")
        return redirect("/")
    product = Product.objects.filter(id=id, seller = user).first()
    if not product:
        return redirect("/")
    product.delete()
    messages.success(request, "Product deleted successfully")
    return redirect("/")