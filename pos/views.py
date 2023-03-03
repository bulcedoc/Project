from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,F,Count
from django.db import IntegrityError
from datetime import datetime,date,timedelta
import pyqrcode
import os

def pos_login(request):
  if request.user.is_authenticated:
        return redirect('pos_billing')
  if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(request=None, username =username, password = password)
      if user is not None:
         login(request,user)
         messages.error(request,'Logged in as '+user.first_name+'\nfor '+user.last_name+' billling.')
         response = redirect('pos_billing')
         return response
      else:
         messages.error(request,'Wrong credentials')
         return render(request, 'pos/pos_login.html')
  else:
    return render(request, 'pos/pos_login.html')

@login_required(login_url='pos_login')
def pos_logout(request):
   logout(request)
   response = redirect('pos_login')
   return response


@login_required(login_url='pos_login')
def pos_home(request):
   u = request.user
   t = date.today()
   y = t -timedelta(days=1)
   d = t -timedelta(days=2)
  
   
      
   td = Bill.objects.filter(bill_user = u ,bill_date = t).aggregate(to = Sum('bill_total'))['to']
   yd = []
   for i in range(0,7):
    y = t -timedelta(days=i)
    c = Bill.objects.filter(bill_user = u ,bill_date = y).aggregate(to = Sum('bill_total'))['to']
    if c:
     yd.append([7-i,Bill.objects.filter(bill_user = u ,bill_date = y).aggregate(to = Sum('bill_total'))['to']])
    else:
     yd.append([7-i,0])
   sd = Bill.objects.filter(bill_user = u ,bill_date = t).values('bill_date').annotate(Count('bill_date'))
   pd = Bill.objects.filter(bill_user = u,bill_date = t).values('bill_payment_type').annotate(Count('bill_payment_type'))
   print(yd)
   pay = [['Payment Method', 'Sale']]
   for i in pd:
     pay.append([i['bill_payment_type'] , Bill.objects.filter(bill_user = u,bill_date = t,bill_payment_type = (i['bill_payment_type'])).aggregate(to = Sum('bill_total'))['to']])
   context = {'tSale':td,
              'nBills':sd,
              'pay':pay,
              'gr':yd,
              'date':date.today(),
              }
   print(pay)
   return render(request, 'pos/pos_home.html',context)

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
      """------------ HEY -------------"""#KOT print function here.
      messages.error(request,"Products added to Table")
      response = redirect('pos_billing')
      return response

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
    tab = int(pk)
    u = request.user
    bill = str(datetime.now().hour)+str(datetime.now().minute)+str(datetime.now().second)
    pros = Cart.objects.filter(cart_table_id = tab,cart_user =u).values()
    ch = []
    for i in pros:
      p = Product.objects.filter(product_user = u,product_id=i['cart_product']).values('product_name','product_price')
      a={}
      a['product'] = p[0]['product_name']
      a['price'] = p[0]['product_price']
      a['quant'] = i['cart_quantity']
      a['p_total'] = a['price']*a['quant']
      ch.append(a)
    if request.method =='POST':
     for p in pros:
      pr = Product.objects.get(product_user= u ,product_id=p['cart_product'])
      if u.first_name == "1":
       try:
        rep = Report.objects.get(rep_user = u,rep_date = str(date.today()) ,rep_product = pr.product_id)
        if rep:
         rep.rep_quantity += p['cart_quantity']
         rep.rep_price += (p['cart_quantity']*pr.product_price)
         rep.save()
       except:
         rep = Report()
         rep.rep_user = u
         rep.rep_date = str(date.today())
         rep.rep_product = pr.product_id
         rep.rep_category = pr.product_category
         rep.rep_quantity += p['cart_quantity']
         rep.rep_price += (p['cart_quantity']*pr.product_price)
         rep.save()
      sale = Sale()
      sale.sale_product_id_id = p['cart_product']
      sale.sale_user = u
      sale.sale_date =  str(date.today())
      sale.sale_bill = bill
      sale.sale_product_name = pr.product_name
      sale.sale_quantity = p['cart_quantity']
      sale.sale_price = pr.product_price
      sale.save()
     sum = Sale.objects.filter(sale_user=u, sale_bill= bill).aggregate(to = Sum(F('sale_price')*F('sale_quantity')))['to']
     Cart.objects.filter(cart_table_id = tab,cart_user =u).delete()
     return pos_bill(request,bill,sum,tab)
    context = {'tab':tab ,'pros_len':len(pros),'bill':bill,'poo':ch}
    return render(request ,'pos/pos_checkout.html', context)


@login_required(login_url='pos_login')
def pos_bill(request,bill,sum,tab):
 try:
   u = request.user
   s = Sale.objects.filter(sale_user= u, sale_bill = int(bill)).values()
   prof = Profile.objects.filter(pro_usr = u).values()
   p = request.POST.get('pay')
   if p == "upi":
    billdata = upi_counter(s,bill,prof,sum)
    """---------- HEY --------------"""#COT print function here.
   else:
    billdata = counter(s,bill,prof,sum,p)
    """---------- HEY --------------"""#COT print function here.
   ch = Bill()
   ch.bill_number = bill
   ch.bill_user = u
   ch.bill_date = str(date.today())
   ch.bill_data = billdata
   ch.bill_total = sum
   ch.bill_payment_type = p
   ch.save()
   messages.error(request,'sales and Bill details added to Databse.')
   t = Table.objects.get(table_user = u , table_id=tab)
   t.table_status = False
   t.save()
   Sale.objects.filter(sale_user= u, sale_bill = int(bill)).delete()
   return render(request,'pos/done.html')
 except IntegrityError as e :
   messages.error(request,'You cannot refresh or interrupt the flow of website.')
   return render(request,'pos/okay.html')



""" --------------------------------------       PRINT FORMATING DONE HERE      -------------------------------------"""

def counter(pr,b,prof,sum,p):
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
 f_n = "Total    "+str(sum).center(30,' ')
 p_n = ("Payment Method   "+str(p)).center(30)
 p_out = "\n\n"+company +"\n\n"+address+"\n"+mob+"\n"+email+"\n\n"+bill+"\n"+line+"\n\n"+ table.get_string()+"\n\n"+line+"\n"+f_n+"\n"+line+"\n\n"+p_n+"\n\n"
 print(p_out)
 return p_out
def upi_counter(pr,b,prof,sum):
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
 f_n = "Total    "+str(sum).center(30,' ')
 p_n = "Payment Method    upi".center(30)
 p_out = "\n\n"+company +"\n\n"+address+"\n"+mob+"\n"+email+"\n\n"+bill+"\n"+line+"\n\n"+ table.get_string()+"\n\n"+line+"\n"+f_n+"\n"+line+"\n\n"+p_n+"\n\n"
 print(p_out)
 upi = "upi://pay?pa="+prof[0]['upi_id']+"&am="+str(sum)
 c_out(upi,b)
 return p_out









@login_required(login_url='pos_login')
def fast_pos_billing(request):
   u =request.user
   products = Product.objects.filter(product_user=u).values()
   categ = Category.objects.filter(category_user=u).values()
   con = {
      'products': products,
      'categ': categ,
      }
   if request.method =='POST':
     bill = str(datetime.now().hour)+str(datetime.now().minute)+str(datetime.now().second)
     p = request.POST.getlist('prod')
     q = request.POST.getlist('quan')
     d = request.POST.get('direc')
     if (len(p)<=0):
        messages.error(request,"No products has been selected")
        res = redirect('fast_pos_billing')
        return res
     else:
      for i in range(len(p)):
       pr = Product.objects.get(product_user= u ,product_id=p[i])
       sale = Sale()
       sale.sale_product_id_id = int(p[i])
       sale.sale_user = u
       sale.sale_date =  str(date.today())
       sale.sale_bill = bill
       sale.sale_product_name = pr.product_name
       sale.sale_quantity = int(q[i])
       sale.sale_price = pr.product_price
       sale.save()
      return redirect('fast_pos_check',bill = bill)
   return render(request,'pos/fast_pos_billing.html',con)

@login_required(login_url='pos_login')
def fast_pos_check(request,bill):
  #from datetime import date
  u = request.user
  dat = str(date.today())
  sale = Sale.objects.filter(sale_user = u,sale_bill=bill).values('sale_product_id','sale_product_name','sale_quantity','sale_price')
  total = Sale.objects.filter(sale_user = u,sale_bill=bill).aggregate(to = Sum(F('sale_price')*F('sale_quantity')))['to']
  context = {'pros_len':len(sale),'bill':bill,'poo':sale,'total':total}
  if request.method == 'POST':
   if u.first_name == "1":
    for p in sale:
     try:
      rep = Report.objects.filter(rep_user = u , rep_date = dat , rep_product = p['sale_product_id']).values('rep_quantity','rep_price')
      if rep:
         rep.rep_quantity += p['sale_quantity']
         rep.rep_price += (p['sale_quantity']*p['sale_price'])
         rep.save()
      else:
         c = Product.objects.get(product_user = u,product_id = p['sale_product_id'])
         rep = Report()
         rep.rep_user = u
         rep.rep_date = dat
         rep.rep_product = c.product_id
         rep.rep_category = c.product_category
         rep.rep_quantity += p['sale_quantity']
         rep.rep_price += (p['sale_quantity'] * p['sale_price'])
         rep.save()
     except:
         c = Product.objects.get(product_user = u,product_id = p['sale_product_id'])
         print(c)
         rep = Report()
         rep.rep_user = u
         rep.rep_date = dat
         rep.rep_product = c.product_id
         rep.rep_category = c.product_category
         rep.rep_quantity += p['sale_quantity']
         rep.rep_price += (p['sale_quantity'] * p['sale_price'])
         rep.save()
   return fast_pos_bill(request,bill,total)  
  return render(request,'pos/fast_pos_checkout.html',context)

@login_required(login_url='pos_login')
def fast_pos_bill(request,bill,sum):
 try:
   u = request.user
   s = Sale.objects.filter(sale_user= u, sale_bill = int(bill)).values()
   prof = Profile.objects.filter(pro_usr = u).values()
   p = request.POST.get('pay')
   if p == "upi":
    billdata = upi_counter(s,bill,prof,sum)
    """---------- HEY --------------"""#COT print function here.
   else:
    billdata = counter(s,bill,prof,sum,p)
   """---------- HEY --------------"""#COT print function here.
   ch = Bill()
   ch.bill_number = bill
   ch.bill_user = u
   ch.bill_date = str(date.today())
   ch.bill_data = billdata
   ch.bill_total = sum
   ch.bill_payment_type = p
   ch.save()
   messages.error(request,'sales and Bill details added to Databse.')
   Sale.objects.filter(sale_user= u, sale_bill = int(bill)).delete()
   return render(request,'pos/fas_done.html')
 except IntegrityError as e :
   messages.error(request,'You cannot refresh or interrupt the flow of website.')
   return render(request,'pos/okay_fast.html')













def c_out(upi,b):
 url = pyqrcode.create(upi)
 url.png(b+".png", scale = 8)
 #p = printer.Network("192.168.1.99")
 #p.text(p_out)
 #p.image(b+".png")
 #p.qr("You can readme from your smartphone")
 #p.barcode('1324354657687','EAN13',64,2,'','')
 #p.cut()
 print("okay done upi ")
 os.remove(b+".png")
 return True