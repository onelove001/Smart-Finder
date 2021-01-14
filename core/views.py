from django.shortcuts import render, redirect
from core.EmailBackEnd import EmailBackEnd
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from core.models import *
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt





def landing_page(request):
    categories = Category.objects.all()
    services = Service.objects.all()
    paginate = Paginator(services, 8)
    p = request.GET.get("page")
    pages = paginate.get_page(p)

    return render(request, 'core_templates/landing_page.html', {"services":services, "pages":pages, "categories":categories})



@csrf_exempt
def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = EmailBackEnd.authenticate(request, email, password)

        if user != None:
            login(request, user)
            if request.user.account_type == "1":
                return redirect("smart_admin_home")

            elif request.user.account_type == "2":
                return redirect("smart_home")

            elif request.user.account_type == "3":
                return redirect("smart_home")

            else:
                return redirect("smart_home")
        else:
            return HttpResponse("Incorrect Details")

    return HttpResponse("False")




@csrf_exempt
def signup_user(request):
    email_key = request.POST.get('email')
    username_key = request.POST.get('username')
    password_key = request.POST.get('password')

    user_buyer = customUser.objects.filter(email = email_key).exists()
    if user_buyer:
        return HttpResponse("False")

    try:
        user_buyer = customUser.objects.create_user(username = username_key, email = email_key, password = password_key, account_type = 2)
        user_buyer.buyer.short_name = "smartbuyer"
        user_buyer.buyer.image = "../media/avatar.jpg"
        user_buyer.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def logout_user(request):
    logout(request)
    return redirect("landing_page")