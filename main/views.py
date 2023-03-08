from django.shortcuts import render,redirect,HttpResponse
from pos.models import *
from django.contrib import messages
def admin_login(request):
   if request.method == 'POST':
      adu = request.POST.get('username')
      pd = request.POST.get('password')
      u = "LJP89%^.26"
      p = "lpo#%nni^(15?66"
      if adu == u and pd == p:
         request.session['adu'] = adu
         print("okay")
         response = redirect('admin_home')
         return response
      else:
         messages.error(request,'Wrong Credentials')
         response = redirect('admin_login')
         return response
   else:
         return render(request,'admin/admin_login.html')
def admin_logout(request):
   try:
      del request.session['adu']
      response = redirect('admin_login')
      return response
   except:
      response = redirect('admin_login')
      return response
def admin_home(request):
 try:
  if request.session['adu']:
    return render(request,'admin/admin_home.html')
 except:
  response = redirect('admin_login')
  return response

def admin_reg(request):
 try:
  if request.session['adu']:
   if request.method == 'POST':
      name = request.POST.get('name')
      bus = request.POST.get('business')
      mob = request.POST.get('mobile')
      em = request.POST.get('email')
      usr = request.POST.get('username')
      psd = request.POST.get('password')
      kip = request.POST.get('kip')
      cip = request.POST.get('cip')
      add = request.POST.get('add')
      upi = request.POST.get('upi')
      sub = request.POST.get('u_t')
      print('oaky ch')
      ch = User.objects.filter(username=usr)
      print('oop')
      print(ch)
      if ch:
       print('oaky 4')
       messages.error(request,'Username already choosen try different one') 
       return render(request,'admin/admin_pos-reg.html')
      else:
       print('oaky 1')
       user = User.objects.create_user(username=usr,password=psd,first_name=sub,last_name=name)
       user.save()
       print('oaky 2')
       cu = User.objects.get(username=usr)
       pro = Profile(counter_ip= cip , kitchen_ip= kip , pro_usr = cu,live = False, mobile = mob ,email = em,business_name = bus,address =add,upi_id=upi)
       pro.save()
       print('oaky 3')
       messages.error(request,'User has been registered')
       response = redirect('admin_home')
       return response
   else:
      print('oaky 8')
      return render(request,'admin/admin_pos-reg.html')
  else:
   print('oaky 9')
   response = redirect('admin_login')
   return response
 except:
   response = redirect('admin_login')
   return response


def admin_edit(request,pk):
 try:
  if request.session['adu']:
   u = User.objects.get(id=pk)
   p = Profile.objects.get(pro_usr = u)
   if request.method == 'POST':
      name = request.POST.get('name')
      bus = request.POST.get('business')
      mob = request.POST.get('mobile')
      em = request.POST.get('email')
      psd = request.POST.get('password')
      kip = request.POST.get('kip')
      cip = request.POST.get('cip')
      add = request.POST.get('add')
      upi = request.POST.get('upi')
      sub = request.POST.get('u_t')
      u.password=psd
      u.first_name=sub
      u.last_name=name
      u.save()
      print("user Okay")
      p.counter_ip= cip 
      p.kitchen_ip= kip 
      p.live = False
      p.mobile = mob 
      p.email = em
      p.business_name = bus
      p.address =add
      p.upi_id=upi
      p.save()
      print('Profile Okay')
      messages.error(request,'User has been updated')
      response = redirect('admin_home')
      return response
   else:
      return render(request,'admin/admin_edit_user.html',{'u':u,'p':p})
 
 except:
   response = redirect('admin_login')
   return response

def admin_sel_u(request):
 try:
  if request.session['adu']:
   pk = User.objects.all()
   return render(request,'admin/admin_sel_u.html',{'pro':pk})
 except:
   response = redirect('admin_login')
   return response
 