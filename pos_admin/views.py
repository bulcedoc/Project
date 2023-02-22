from django.shortcuts import render,redirect
from pos.models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


def pos_admin_login(request):
  if request.user.is_authenticated:
        return redirect('pos_admin_home')
  if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(request=None, username =username, password = password)
      if user is not None:
        pik = Profile.objects.get(pro_usr = user.id)
        if pik.live == False:
         login(request,user)
         pik.live = True
         pik.save()
         response = redirect('pos_admin_home')
         return response
        else:
         messages.error(request,'you have already logged in another device/pos')
         return render(request, 'pos_admin/pos_admin_login.html')
      else:
         messages.error(request,'Wrong credentials')
         return render(request, 'pos_admin/pos_admin_login.html')
  else:
    return render(request, 'pos_admin/pos_admin_login.html')

@login_required
def pos_admin_logout(request):
   pik = Profile.objects.get(pro_usr = request.user.id)
   pik.live = False
   pik.save()
   logout(request)
   response = redirect('pos_admin_login')
   return response

@login_required(login_url="pos_admin_login")
def pos_admin_home(request):
    u = request.user.first_name
    con = {
        'user':u
     }
    return render(request,'pos_admin/pos_admin_home.html',con)

@login_required(login_url="pos_admin_login")
def pos_admin_add_cat(request):
    if request.method == 'POST':
     cat = request.POST.get('name')
     entry = Category()
     entry.category_name =cat
     entry.category_user = request.user
     entry.save()
     messages.error(request,'Category added successfully.')
     u = request.user.first_name
     con = {
        'user':u
     }
     return render(request,'pos_admin/pos_admin_add_cat.html',con)
    else:
     u = request.user.first_name
     con = {
        'user':u
     }
     return render(request,'pos_admin/pos_admin_add_cat.html',con)

@login_required(login_url="pos_admin_login")
def pos_admin_add_product(request):
    if request.method == 'POST':
     p = request.POST.get('name')
     f = request.POST.get('fav')
     c = request.POST.get('cat')
     pr = request.POST.get('price')
     entry = Product()
     entry.product_name = p
     entry.product_price = pr
     if f == "1":
      entry.product_fav = True
     else:
      entry.product_fav = False 
     entry.product_category_id = int(c)
     entry.product_user = request.user
     entry.save()
     messages.error(request,'Product added successfully.')
     u = request.user
     i = request.user
     cat = Category.objects.filter(category_user=i).values()
     con = {
        'user':u,
        'cat':cat
     }
     return render(request,'pos_admin/pos_admin_add_product.html',con)
    else:
     i = request.user
     cat = Category.objects.filter(category_user=i).values()
     if cat:
      con = {
        'user':i,
        'cat':cat
      }
      return render(request,'pos_admin/pos_admin_add_product.html',con)
     else:
      messages.error(request,"You don't have any category, product mush be categorized.")
      res = redirect('pos_admin_home')
      return res

@login_required(login_url="pos_admin_login")
def pos_admin_add_table(request):
    if request.method == 'POST':
     t = request.POST.get('name')
     entry = Table()
     entry.table_user = request.user
     entry.table_name = t
     entry.save()
     messages.error(request,'Table added successfully.')
     u = request.user.first_name
     con = {
        'user':u
     }
     return render(request,'pos_admin/pos_admin_add_table.html')
    else:
     u = request.user.first_name
     con = {
        'user':u
     }
     return render(request,'pos_admin/pos_admin_add_table.html')