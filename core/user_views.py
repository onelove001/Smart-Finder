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
    buyers_count = Buyer.objects.all().count()
    sellers_count = Seller.objects.all().count()
    services_count = Service.objects.all().count()
    categories_count = Category.objects.all().count()
    all_members = customUser.objects.all().count()


    context = {
        "categories":categories,
        "categories_count":categories_count,
        "sellers_count":sellers_count,
        "buyers_count":buyers_count,
        "services_count":services_count,
        "all_members":all_members,
    }

    return render(request, 'user_templates/home_content.html', context)


def freelancers_page(request, category_idd):
    categories = Category.objects.all()
    services = Service.objects.filter(category = category_idd)
    serv = Service.objects.filter(category = category_idd).count()
    freelancers = Seller.objects.filter(category = category_idd).count()

    paginate = Paginator(services, 2)
    p = request.GET.get("page")
    pages = paginate.get_page(p)

    context = {"categories":categories, "services":services, "serv":serv, "freelancers":freelancers, "pages":pages}
    return render(request, 'user_templates/freelancers.html', context)



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
        service = Service.objects.filter(owner = seller.id)
        if service.exists():
            empty = 1
        else:
            empty = 0
    
        try:
            buyers = []
            service_co = Service.objects.filter(owner = seller.id, ordered = "ordered")
            for serv in service_co:
                orders = Order.objects.filter(service_ordered = serv.id)
                for s in orders:
                    buyers.append(s)
                    
            service_count = len(buyers)
            context = {"seller":seller, "service_count":service_count, "buyers":buyers, "empty":empty, "service":service}

        except:
            context = {"seller":seller}

    return render(request, "user_templates/dashboard.html", context)



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
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        shortname = request.POST.get("shortname")
        address = request.POST.get("address")
        description = request.POST.get("description")
        phone = request.POST.get("phone")

        if request.FILES.get('image', False):
            profile_image = request.FILES['image']
            fs = FileSystemStorage()
            profile_image_save = fs.save(profile_image.name, profile_image)
            image_url = fs.url(profile_image_save)
        else:
            image_url = None

        try:
            user = customUser.objects.get(id = user_id)
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            seller = Seller.objects.get(admin = user.id)
            seller.phone_number = phone
            seller.short_name = shortname
            seller.address = address
            seller.description = description
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
        shortname = request.POST.get("shortname")

        if request.FILES.get('image', False):
            profile_image = request.FILES['image']
            fs = FileSystemStorage()
            profile_image_save = fs.save(profile_image.name, profile_image)
            image_url = fs.url(profile_image_save)
        else:
            image_url = None
        try:
            user = customUser.objects.get(id = user_id)

            buyer = Buyer.objects.get(admin = user.id)
            buyer.short_name = shortname
            if image_url != None:
                buyer.image = image_url
            buyer.save()

            messages.success(request, "Profile Update Successfull")
            return redirect(request.META.get("HTTP_REFERER"))

        except:
            messages.error(request, "Profile Update Failed")
            return redirect(request.META.get("HTTP_REFERER"))

    return HttpResponse("Request cannot be processed")


@login_required
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
            service = Service(owner=seller, description=description, charge=charge, title=title,  plan = plan_obj, category=cat_obj, sub_category=sub_cat_obj, image1=image1_url, image2=image2_url, image3=image3_url)
            service.save()
            messages.success(request, "Service Created Successfully")
            return redirect(request.META.get("HTTP_REFERER"))

        except:
            messages.error(request, "Failed To Create Service")
            return redirect(request.META.get("HTTP_REFERER"))

    return HttpResponse("Request cannot be processed")



@login_required
def service_detail(request, service_id):
    service = Service.objects.get(id = service_id)
    ratings = star_rating.objects.all()
    reviews = Reviews.objects.filter(seller_id = service.owner.id).count()
    

    return render(request, "user_templates/service_detail.html", {"service":service, "ratings":ratings, "reviews":reviews})



def get_category(request, category_id):
    categories = Category.objects.all()
    category_id = Category.objects.get(id = category_id)
    services = Service.objects.filter(category = category_id)
    paginate = Paginator(services, 4)
    p = request.GET.get("page")
    pages = paginate.get_page(p)

    return render(request, 'user_templates/get_category_page.html', {"services":services, 'pages':pages, 'categories':categories})



@login_required
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



def user_review_save(request):
    if request.method == "POST":
        seller = request.POST.get('user')
        review = request.POST.get('review')
        rate = request.POST.get('rate')
        service = request.POST.get('service')

        print(" ############### ", rate)

        seller_obj = customUser.objects.get(id = seller)
        service_obj = Service.objects.get(id = service)
        user_obj = customUser.objects.get(id = request.user.id)
        seller_id = Seller.objects.get(admin = seller_obj.id)
        rate_obj = star_rating.objects.get(id = rate)

        try:
            review_obj = Reviews(seller_id = seller_id, service_id = service_obj, user_id = user_obj, rating = rate_obj, review_content = review)
            review_obj.save()
            return redirect(request.META.get("HTTP_REFERER"))

        except:
            return HttpResponse("False")
    return HttpResponse("<h2> Cannot process this request </h2>")



@login_required
def user_service_order(request):
    if request.method == "POST":
        service_id = request.POST.get("service_id")
        service_obj = Service.objects.get(id = service_id)
        user = request.user.id
        user_obj = customUser.objects.get(id = user)

        try:
        
            order = Order(user_order = user_obj, service_ordered = service_obj, status = "ordered")
            order.save()
            order_obj = Order.objects.filter(user_order = user_obj).first()
            service_obj.orders = order_obj
            service_obj.ordered = "ordered"
            service_obj.save()

            messages.success(request, " Service ordered successfully! ")
            return redirect(request.META.get("HTTP_REFERER"))

        except:
            messages.error(request, " Error processing this order ")
            return redirect(request.META.get("HTTP_REFERER"))

    return HttpResponse(" <h2> This request cannot be processed </h2> ")



def seller_profile(request, seller_id):
    seller = Seller.objects.get(id = seller_id)
    services = Service.objects.filter(owner = seller.id).count()
    reviews = Reviews.objects.filter(seller_id = seller.id)
    reviewss = Reviews.objects.filter(seller_id = seller.id).count()
    
    paginator = Paginator(reviews, 3)
    p = request.GET.get("page")
    pages = paginator.get_page(p)

    context = { "seller":seller, "reviews":reviews, "pages":pages, "services":services, "reviewss":reviewss}
    return render(request, "user_templates/seller_profile.html", context)



def seller_reviews(request):
    user_id = request.user.id
    seller = Seller.objects.get(admin = user_id)
    reviews = Reviews.objects.filter(seller_id = seller.id)
    reviewss = Reviews.objects.filter(seller_id = seller.id).count()

    paginator = Paginator(reviews, 2)
    p = request.GET.get("page")
    pages = paginator.get_page(p)

    return render(request, "user_templates/seller_reviews.html", {"reviews":reviews, "pages":pages, "reviewss":reviewss})