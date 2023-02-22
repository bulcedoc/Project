from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,F
from django.db import IntegrityError

def pos_login(request):
  if request.user.is_authenticated:
        return redirect('pos_billing')
  if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(request=None, username =username, password = password)
      if user is not None:
        pik = Profile.objects.get(pro_usr = user.id)
        #if pik.live == False:
        login(request,user)
         #pik.live = True
         #pik.save()
         #messages.error(request,'logged in as '+user.first_name+' for '+user.last_name+' billling.')
        response = redirect('pos_billing')
        return response
        #else:
         #messages.error(request,'you have already logged in another device')
         #return render(request, 'pos/pos_login.html')
      else:
         messages.error(request,'Wrong credentials')
         return render(request, 'pos/pos_login.html')
  else:
    return render(request, 'pos/pos_login.html')

@login_required(login_url='pos_login')
def pos_logout(request):
   pik = Profile.objects.get(pro_usr = request.user.id)
   pik.live = False
   pik.save()
   logout(request)
   response = redirect('pos_login')
   return response

@login_required(login_url='pos_login')
def pos_billing(request):
   u =request.user
   products = Product.objects.filter(product_user=u).values()
   categ = Category.objects.filter(category_user=u).values()
   carts = Table.objects.filter(table_user =u).values()
   con = {
      'products': products,
      'categ': categ,
      'carts':carts,
      }
   return render(request,'pos/pos_billing.html',con)
         
@login_required(login_url='pos_login')
def pos_cart(request):
      p = request.POST.getlist('prod')
      q = request.POST.getlist('quan')
      c = int(request.POST.get('cart'))
      d = request.POST.get('direc')
      if (len(p)<=0):
        messages.error(request,"No products has been selected")
        res = redirect('pos_billing')
        return res
      else:  
        u = request.user
        for i,j in zip(p,q):
           cart = Cart.objects.filter(cart_user= u,cart_table_id=c,cart_product=i)
           if not cart:
              table = Table.objects.get(table_user =u ,table_id =c)
              cart = Cart()
              cart.cart_table_id = table
              cart.cart_user = u
              cart.cart_product = int(i)
              cart.cart_quantity = int(j)
              cart.cart_direc = d
              cart.save()
              table.table_status = True
              table.save()
           else:
              cat = Cart.objects.get(cart_user= u,cart_table_id=c,cart_product=i)
              cat.cart_quantity += int(j) 
              cart.cart_direc = d  
              cat.save()
      messages.error(request,"Products added to Table")
      response = redirect('pos_billing')
      return response
"""----------------------------------------all clear-----------------------------------------------"""
@login_required(login_url='pos_login')
def pos_home(request):
   return render(request, 'pos/pos_home.html')

@login_required(login_url='pos_login')
def pos_checkouts(request):
   u = request.user
   check = Table.objects.filter(table_user = u, table_status = True).values() 
   if not check:
      messages.error(request,'You have no orders to checkout.')
      return render(request ,'pos/okay.html')
   context = {'checkouts' : check}
   return render(request ,'pos/pos_checkouts.html',context)

@login_required(login_url='pos_login')
def pos_tables(request):
   u = request.user
   o = Table.objects.filter(table_user = u, table_status = True).values()
   a = Table.objects.filter(table_user = u, table_status = False).values()
   context = {'open':o,'av':a}
   return render(request ,'pos/pos_tables.html',context)

@login_required(login_url='pos_login')
def pos_b_t(request,pi,pn):
   u =request.user
   n = {'id':pi,
        'name':pn,
       }
   products = Product.objects.filter(product_user=u).values()
   categ = Category.objects.filter(category_user=u).values()
   carts = Table.objects.filter(table_user =u).values()
   con = {
      'products': products,
      'categ': categ,
      'carts':carts,
      'n':n,
      }
   return render(request,'pos/pos_billing.html',con)

@login_required(login_url='pos_login')
def pos_checkout(request,pk):
    from datetime import datetime
    tab = int(pk)
    u = request.user
    bill = str(datetime.now().hour)+str(datetime.now().minute)+str(datetime.now().second)
    pros = Cart.objects.filter(cart_table_id = tab,cart_user =u).values()
    if request.method =='POST':
     for p in pros:
      pr = Product.objects.get(product_user= u ,product_id=p['cart_product'])
      sale = Sale()
      sale.sale_product_id_id = p['cart_product']
      sale.sale_user = u
      sale.sale_year =  str(datetime.now().year)
      sale.sale_month =  str(datetime.now().month)
      sale.sale_day =  str(datetime.now().day)
      sale.sale_bill = int(bill)
      sale.sale_price = pr.product_price
      sale.sale_product_name = pr.product_name
      sale.sale_quantity = p['cart_quantity']
      sale.save()
     sum = Sale.objects.filter(sale_user=u, sale_bill= bill).aggregate(to = Sum(F('sale_price')*F('sale_quantity')))['to']
     Cart.objects.filter(cart_table_id = tab,cart_user =u).delete()
     return pos_bill(request,bill,sum,tab)
    context = {'tab':tab ,'pros_len':len(pros),'pros':pros}
    return render(request ,'pos/pos_checkout.html', context)


@login_required(login_url='pos_login')
def pos_bill(request,bill,sum,tab):
 try:
   from datetime import date
   u = request.user
   s = Sale.objects.filter(sale_user= u, sale_bill = int(bill)).values()
   prof = Profile.objects.filter(pro_usr = u).values()
   billdata = counter(s,bill,sum,prof)
   ch = Bill()
   ch.bill_number = bill
   ch.bill_user = u
   ch.bill_date = str(date.today())
   ch.bill_data = billdata
   ch.bill_total = sum
   ch.bill_payment_type = request.POST.get('pay')
   ch.save()
   messages.error(request,'sales and Bill details added to Databse.')
   t = Table.objects.get(table_user = u , table_id=tab)
   t.table_status = False
   t.save()
   return render(request,'pos/done.html')
 except IntegrityError as e :
   messages.error(request,'You cannot refresh or interrupt the flow of website.')
   return render(request,'pos/okay.html')



""" --------------------------------------       PRINT FORMATING DONE HERE      -------------------------------------"""

def counter(pr,b,s,prof):
 from prettytable import PrettyTable
 from datetime import date
 import textwrap
 company = str(prof[0]['business_name']).center(32,' ')
 address = str(prof[0]['address']).center(30,' ')
 address = textwrap.fill(address,width=30)
 mob = str(prof[0]['mobile']).center(30,' ')
 mob = textwrap.fill(mob,width=30)
 email = str(prof[0]['email']).center(30,' ')
 email = textwrap.fill(email,width=30)
 day = str(date.today()).rjust(10,' ')
 bill = "B.No "+b+"".ljust(10,' ')
 bill = bill+day
 table = PrettyTable(['Product','Price','Qty','Amt'])
 for i in pr:
  c = textwrap.fill(i['sale_product_name'],width=10)
  table.add_row([c,i['sale_price'],i['sale_quantity'],i['sale_price']*i['sale_quantity']])
 table.border = False
 table.padding_width = 1
 line = "-".center(30,'-')
 f_n = "Total    "+str(s).center(30,' ')
 p_out = "\n\n"+company +"\n\n"+address+"\n"+mob+"\n"+email+"\n\n"+bill+"\n"+line+"\n\n"+ table.get_string()+"\n\n"+line+"\n"+f_n+"\n"+line+"\n\n"
 return p_out
