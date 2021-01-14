from django.shortcuts import *
from django.http import *
from core.models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json



def smart_home(request):
    categories = Category.objects.all()
    services = Service.objects.all()
    paginate = Paginator(services, 8)
    p = request.GET.get("page")
    pages = paginate.get_page(p)

    return render(request, 'user_templates/home_page.html', {"services":services, "pages":pages, "categories":categories})



def seller_page(request):
    return render(request, 'user_templates/seller_page.html', {})




def become_seller(request):
    user = request.user
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    languages = Language.objects.all()
    levels = Xperienece_level.objects.all()

    return render(request, "user_templates/become_seller.html", {"user":user, "sub_categories":sub_categories, "categories":categories, "languages":languages, "levels":levels})


@csrf_exempt
def fetch_subcategories(request):
    category = request.POST.get("category")
    category_obj = Category.objects.get(id = category)
    check_if_exist = SubCategory.objects.filter(category = category_obj).exists()
    if check_if_exist:
        sub_categories = SubCategory.objects.filter(category = category_obj)
        list_data = []
        for categories in sub_categories:
            data = {"id":categories.id, "sub_category_title":categories.sub_category_title}
            list_data.append(data)
        return JsonResponse(json.dumps(list_data), content_type = "application/json", safe=False)

    else:
        return JsonResponse(json.dumps("False"), content_type = "application/json", safe = False)
   
    
def become_seller_save(request):
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    cellphone = request.POST.get("cellphone")
    shortname = request.POST.get("shortname")
    address = request.POST.get("address")
    level = request.POST.get("level")
    category = request.POST.get("cat")
    sub_category = request.POST.get("sub_cat")
    language = request.POST.get("lang")
    gender = request.POST.get("gender")
    description = request.POST.get("description")
    profile_image = request.FILES['image']

    fs = FileSystemStorage()
    profile_image_save = fs.save(profile_image.name, profile_image)
    image_url = fs.url(profile_image_save)

    cat_obj     = Category.objects.get(id = category)
    subcat_obj  = SubCategory.objects.get(id = sub_category)
    lang_obj    = Language.objects.get(id = language)
    level_obj   = Xperienece_level.objects.get(id = level)
    user = request.user.id

    try:

        user_seller = customUser.objects.get(id = user)
        user_seller.account_type = "3"
        user_seller.first_name = firstname
        user_seller.last_name = lastname
        user_seller.save()

        seller = Seller(admin = user_seller, short_name = shortname, image = image_url, category = cat_obj, phone_number = cellphone, address = address, gender = gender, description = description, language = lang_obj, experience_level = level_obj, sub_category = subcat_obj)
        seller.save()
        buyer = Buyer.objects.get(admin = user)
        buyer.delete()
        return redirect("user_profile")

    except:
        messages.error(request, "Failed To Create")
        return redirect(request.META.get("HTTP_REFERER"))
    
    return HttpResponse("<h2> Invalid Request </h2>")



@login_required
def user_profile(request):

    if request.user.account_type == '2':
        user = customUser.objects.get(id = request.user.id)
        buyer = Buyer.objects.get(admin = user.id)
        context = {"buyer":buyer}

    if request.user.account_type == '3':
        user = customUser.objects.get(id = request.user.id)
        seller = Seller.objects.get(admin = user.id)
        context = {"seller":seller}

    return render(request, "user_templates/user_profile.html", context)



@login_required
def update_profile_seller(request):
    user = request.user.id
    seller = Seller.objects.get(admin = user)
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    languages = Language.objects.all()
    levels = Xperienece_level.objects.all()
    context = {"seller":seller, "categories":categories, "sub_categories":sub_categories, "languages":languages, "levels":levels}
    return render(request, "user_templates/update_seller_profile.html", context)



@login_required
def update_profile_buyer(request):
    user = request.user.id
    buyer = Buyer.objects.get(admin = user)

    context = {"buyer":buyer}
    return render(request, "user_templates/update_buyer_profile.html", context)




def update_profile_seller_save(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        shortname = request.POST.get("shortname")
        address = request.POST.get("address")
        description = request.POST.get("description")
        phone = request.POST.get("phone")
        level = request.POST.get("level")
        lang = request.POST.get("lang")
        gender = request.POST.get("gender")

        if request.FILES.get('image', False):
            profile_image = request.FILES['image']
            fs = FileSystemStorage()
            profile_image_save = fs.save(profile_image.name, profile_image)
            image_url = fs.url(profile_image_save)
        else:
            image_url = None

        try:
            lang_obj = Language.objects.get(id = lang)
            level_obj = Xperienece_level.objects.get(id= level)

            user = customUser.objects.get(id = user_id)
            user.username = username
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            seller = Seller.objects.get(admin = user.id)
            seller.phone_number = phone
            seller.short_name = shortname
            seller.address = address
            seller.description = description
            seller.language = lang_obj
            seller.experience_level = level_obj
            seller.gender = gender
            if image_url != None:
                seller.image = image_url
            seller.save()
            messages.success(request, "Profile Update Successfull")
            return redirect(request.META.get("HTTP_REFERER"))

        except:
            messages.error(request, "Profile Update Failed")
            return redirect(request.META.get("HTTP_REFERER"))

    return HttpResponse("Request cannot be processed")



def update_profile_buyer_save(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        username = request.POST.get("username")

        if request.FILES.get('image', False):
            profile_image = request.FILES['image']
            fs = FileSystemStorage()
            profile_image_save = fs.save(profile_image.name, profile_image)
            image_url = fs.url(profile_image_save)
        else:
            image_url = None
        try:
            user = customUser.objects.get(id = user_id)
            user.username = username
            user.save()

            buyer = Buyer.objects.get(admin = user.id)
            if image_url != None:
                buyer.image = image_url
            buyer.save()

            messages.success(request, "Profile Update Successfull")
            return redirect(request.META.get("HTTP_REFERER"))

        except:
            messages.error(request, "Profile Update Failed")
            return redirect(request.META.get("HTTP_REFERER"))

    return HttpResponse("Request cannot be processed")



def create_service_(request):
    user = request.user.id
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    plans = Plan.objects.all()
    owner = Seller.objects.get(admin = user)
    return render(request, "user_templates/create_servic.html", {"plans":plans, "categories":categories, "sub_categories":sub_categories, "owner":owner})



def create_service_save(request):
    if request.method == "POST":
        owner_id = request.POST.get("owner_id")
        title = request.POST.get("title")
        charge = request.POST.get("charge")
        function = request.POST.get("function")
        cat = request.POST.get("cat")
        sub_cat = request.POST.get("sub_cat")
        plan = request.POST.get("plan")
        description = request.POST.get("description")
        image1 = request.FILES["image1"]
        image2 = request.FILES["image2"]
        image3 = request.FILES["image3"]

        fs = FileSystemStorage()
        profile_image1_save = fs.save(image1.name, image1)
        profile_image2_save = fs.save(image2.name, image2)
        profile_image3_save = fs.save(image3.name, image3)

        image1_url = fs.url(profile_image1_save)
        image2_url = fs.url(profile_image2_save)
        image3_url = fs.url(profile_image3_save)
        
        cat_obj = Category.objects.get(id = cat)
        plan_obj = Plan.objects.get(id = plan)
        sub_cat_obj = SubCategory.objects.get(id = sub_cat)
        user= customUser.objects.get(id = owner_id)
        seller = Seller.objects.get(admin = user.id)
        
        try:
            service = Service(owner=seller, description=description, charge=charge, title=title, function=function, plan = plan_obj, category=cat_obj, sub_category=sub_cat_obj, image1=image1_url, image2=image2_url, image3=image3_url)
            service.save()
            messages.success(request, "Service Created Successfully")
            return redirect(request.META.get("HTTP_REFERER"))

        except:
            messages.error(request, "Failed To Create Service")
            return redirect(request.META.get("HTTP_REFERER"))

    return HttpResponse("Request cannot be processed")



def seller_profile_detail(request, service_id):
    service = Service.objects.get(id = service_id)
    return render(request, "user_templates/seller_profile_detail.html", {"service":service})



def get_category(request, category_id):
    categories = Category.objects.all()
    category_id = Category.objects.get(id = category_id)
    services = Service.objects.filter(category = category_id)
    paginate = Paginator(services, 4)
    p = request.GET.get("page")
    pages = paginate.get_page(p)

    return render(request, 'user_templates/get_category_page.html', {"services":services, 'pages':pages, 'categories':categories})


def search(request):
    if request.method == "POST":
        search = request.POST.get('search')
        print(search)

        try:
            category = Category.objects.get(category_title = search)
            id = category.id
            return redirect('get_category/'+str(id))

        except:
            return redirect('smart_home')

    else:
        return HttpResponse('Not a valid request')




