from django.shortcuts import render
from django.contrib.auth import logout

def err_404(request, exception):
   logout(request)
   return render(request, 'error/404.html', status=404)
def err_500(request):
   logout(request)
   return render(request, 'error/error_handler.html', status=500)
def err_400(request, exception):
   logout(request)
   return render(request,'error/error_handler.html')
def csrf_failure(request, reason=""):
   logout(request)
   return render(request,'error/csrf_error.html')
def home(request):
   return render(request,'sadada/home.html')