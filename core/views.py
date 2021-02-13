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
    buyers_count = Buyer.objects.all().count()
    sellers_count = Seller.objects.all().count()
    services_count = Service.objects.all().count()
    services = Service.objects.all()
    categories_count = Category.objects.all().count()
    all_members = customUser.objects.all().count()


    paginate = Paginator(services, 4)
    p = request.GET.get("page")
    pages = paginate.get_page(p)

    context = {
        "categories":categories,
        "categories_count":categories_count,
        "sellers_count":sellers_count,
        "buyers_count":buyers_count,
        "services_count":services_count,
        "all_members":all_members,
        "services":services,
        "pages":pages,

    }

    return render(request, 'core_templates/landing_page2.html', context)



# @csrf_exempt
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
                return redirect("page_404")
        else:
            return redirect("page_404")

    return redirect("page_404")




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


def search22(request):
    if request.method == "POST":
        search = request.POST.get('search22')
        print(search)

        try:
            category = Category.objects.get(category_title = search)
            id = category.id
            return redirect('search_result', search_id = id)

        except:
            return redirect('page_404')
    return redirect('page_404')


def search_result(request, search_id):
    services = Service.objects.filter(category=search_id)
    freelancers = Seller.objects.all().count()
    serv = Service.objects.filter(category=search_id).count()

    paginate = Paginator(services, 2)
    p = request.GET.get("page")
    pages = paginate.get_page(p)

    return render(request, "core_templates/search_result.html", {"services":services, "serv":serv, "freelancers":freelancers, "pages":pages})
    