from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
import json

def index(request):
    allProds = []
    catprods = Product.objects.values('category')
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-n//4)
        allProds.append([prod,range(1,nSlides),nSlides])
    params = {'allProds':allProds}
    return render(request,'shop/index.html',params)

def about(request):
    return render(request,'shop/aboutus.html') 

def contact(request):
    if request.method=="POST":
        print(request)
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
    return render(request,'shop/contact.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get("orderId",'')
        email = request.POST.get("email",'')
        try :
            order = Orders.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates=[]
                for item in update:
                    updates.append({'text': item.update_desc,'time':item.timestamp})
                    response = json.dumps(updates,default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')  
        except Exception as e:
            return HttpResponse('{}')                     
    return render(request,'shop/tracker.html')

def search(request):
    return render(request,'shop/search.html')   

def productView(request,myid):
    product = Product.objects.filter(id=myid)
    return render(request,'shop/prodview.html',{'product':product[0]})  

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        address = request.POST.get('address1','')+" "+request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone','')
        order = Orders(items_json=items_json,name=name,email=email,phone=phone,address=address,city=city,state=state,zip_code=zip_code)
        order.save()
        thank = True
        update = OrderUpdate(order_id=order.order_id,update_desc="The order has been placed")
        update.save()
        id = order.order_id
        return render(request,'shop/checkout.html',{'thank':thank,"id":id})
    return render(request,'shop/checkout.html')              
# Create your views here.

def cart(request):
    key = request.COOKIES.get('key')
    # products = Product.objects.all()
    Cartprod = {}
    print(key)
    for i in range(4,len(key)-1,8):
        Cartprod[key[i:i+1]] = [key[i+3:i+4],Product.objects.filter(id=key[i:i+1])]
        # Cartprod.append(Product.objects.filter(id=key[i:i+1]))
    print(Cartprod)    
    param = {'Cartprod':Cartprod}
    return render(request,'shop/cart.html',param)