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
    
    if request.user.account_type == "3":
        user_1 = request.user.id 
        seller = Seller.objects.get(admin = user_1)
        reviews = Reviews.objects.filter(seller_id = seller.id).count()
        context = {"reviews":reviews}

    elif request.user.account_type == "2":
        user = request.user
        categories = Category.objects.all()
        sub_categories = SubCategory.objects.all()
        languages = Language.objects.all()
        levels = Xperienece_level.objects.all()

        context = {"user":user, "sub_categories":sub_categories, "categories":categories, "languages":languages, "levels":levels}

    return render(request, "user_templates/become_seller.html", context)


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
        reviews = Reviews.objects.filter(seller_id = seller.id).count()
        service = Service.objects.filter(owner = seller.id)
        if service.exists():
            empty = 1
        else:
            empty = 0
    
        # try:
        #     buyers = []
        #     service_co = Service.objects.filter(owner = seller.id, ordered = "ordered")
        #     for serv in service_co:
        #         orders = Order.objects.filter(service_ordered = serv.id)
        #         for s in orders:
        #             buyers.append(s)
                    
        #     service_count = len(buyers)
        context = {"seller":seller, "empty":empty, "service":service, "reviews":reviews}

        # except:
        #     context = {"seller":seller}

    return render(request, "user_templates/dashboard.html", context)


@login_required
def update_profile_seller(request):
    user = request.user.id
    seller = Seller.objects.get(admin = user)
    reviews = Reviews.objects.filter(seller_id = seller.id).count()
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    languages = Language.objects.all()
    levels = Xperienece_level.objects.all()

    context = {
        "seller":seller, 
        "categories":categories, 
        "sub_categories":sub_categories, 
        "languages":languages, 
        "levels":levels,
        "reviews":reviews
    }
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
    seller = Seller.objects.get(admin = user)
    reviews = Reviews.objects.filter(seller_id = seller.id).count()
    sub_categories = SubCategory.objects.all()
    days = Delivery_days.objects.all()
    plans = Plan.objects.all()
    owner = Seller.objects.get(admin = user)
    return render(request, "user_templates/create_servic.html", {"days":days, "reviews":reviews, "plans":plans, "categories":categories, "sub_categories":sub_categories, "owner":owner})


def create_service_save(request):
    if request.method == "POST":
        owner_id = request.POST.get("owner_id")
        title = request.POST.get("title")
        charge = request.POST.get("charge")
        days = request.POST.get("days")
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
        days_obj = Delivery_days.objects.get(id = days)
        plan_obj = Plan.objects.get(id = plan)
        sub_cat_obj = SubCategory.objects.get(id = sub_cat)
        user= customUser.objects.get(id = owner_id)
        seller = Seller.objects.get(admin = user.id)
        
        try:
            service = Service(owner=seller, days = days_obj, description=description, charge=charge, title=title,  plan = plan_obj, category=cat_obj, sub_category=sub_cat_obj, image1=image1_url, image2=image2_url, image3=image3_url)
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


@login_required
def get_category(request, category_id):
    categories = Category.objects.all()
    category_id = Category.objects.get(id = category_id)
    sellers = Seller.objects.filter(category = category_id)
    freelancers = Seller.objects.filter(category = category_id).count()
    services = Service.objects.filter(category = category_id).count()

    paginate = Paginator(sellers, 2)
    p = request.GET.get("page")
    pages = paginate.get_page(p)

    return render(request, 'user_templates/get_category_page.html', {"freelancers":freelancers, "services":services, "sellers":sellers, 'pages':pages, 'categories':categories})


@login_required
def search(request):
    if request.method == "POST":
        search = request.POST.get('search')
        search2 = request.POST.get('search2')

        if search:

            try:
                category = Category.objects.get(category_title = search)
                id = category.id
                return redirect('get_category', category_id = id)

            except:
                return redirect('smart_home')

        if search2:
            try:
                category = Category.objects.get(category_title = search2)
                id = category.id
                return redirect('get_category', category_id = id)

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
        seller_id = request.POST.get("seller_id")
        service_obj = Service.objects.get(id = service_id)

        user = request.user.id
        user_obj = customUser.objects.get(id = user)
        seller_obj = Seller.objects.get(id = seller_id)

        try:
        
            order = Order(user_order = user_obj, seller_id = seller_obj, service_ordered = service_obj, status = "ordered")
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
    reviewss = Reviews.objects.filter(seller_id = seller.id)
    reviews = Reviews.objects.filter(seller_id = seller.id).count()

    paginator = Paginator(reviewss, 2)
    p = request.GET.get("page")
    pages = paginator.get_page(p)

    return render(request, "user_templates/seller_reviews.html", {"reviews":reviews, "pages":pages, "reviewss":reviewss})


def manage_services(request):

    user = request.user.id
    seller = Seller.objects.get(admin = user)
    services = Service.objects.filter(owner = seller.id)
    servicesss = Service.objects.filter(owner = seller.id).count()
    reviews = Reviews.objects.filter(seller_id = seller.id).count()

    paginate = Paginator(services, 3)
    p = request.GET.get("page")
    pages = paginate.get_page(p)

    context = {"services":services, "reviews":reviews, "pages":pages, "servicesss":servicesss}

    return render(request, "user_templates/manage_services.html", context)


def edit_service(request, service_edit_id):
    service = Service.objects.get(id = service_edit_id)
    user = request.user.id
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    plans = Plan.objects.all()
    days = Delivery_days.objects.all()
    seller = Seller.objects.get(admin = user)
    reviews = Reviews.objects.filter(seller_id = seller.id).count()

    context = {"days":days, "service":service, "reviews":reviews, "plans":plans, "categories":categories, "sub_categories":sub_categories}

    return render(request, "user_templates/edit_service.html", context)


def delete_service(request, service_delete_id):
    service = Service.objects.get(id = service_delete_id)
    service.delete()

    return redirect(request.META.get("HTTP_REFERER"))


def edit_service_save(request):
    if request.method == "POST":
        title = request.POST.get("title")
        service_id = request.POST.get("service_id")
        charge = request.POST.get("charge")
        plan = request.POST.get("plan")
        days = request.POST.get("days")
        description = request.POST.get("description")

        if request.FILES.get('image1', False):
            profile_image = request.FILES['image1']
            fs = FileSystemStorage()
            profile_image_save = fs.save(profile_image.name, profile_image)
            image_url1 = fs.url(profile_image_save)
        else:
            image_url1 = None

        plan_obj = Plan.objects.get(id = plan)
        days_obj = Delivery_days.objects.get(id = days)
        
        try:
            service = Service.objects.get(id = service_id)
            service.title = title
            service.charge = charge
            service.plan = plan_obj
            service.days = days_obj
            service.description = description
            if image_url1 != None:
                service.image1 = image_url1

            service.save()
            messages.success(request, "Service Updated Successfully")
            return redirect(request.META.get("HTTP_REFERER"))

        except:
            messages.error(request, "Failed To Update Service")
            return redirect(request.META.get("HTTP_REFERER"))

    return HttpResponse("Request cannot be processed")


def buyer_profile(request, buyer_id):
    user_id = customUser.objects.get(id = buyer_id)
    buyer = Buyer.objects.get(id = user_id.id)
    return render(request, "user_templates/buyer_profile.html", {"buyer":buyer})


def active_orders(request):

    user = request.user.id
    seller = Seller.objects.get(admin = user)
    reviews = Reviews.objects.filter(seller_id = seller.id).count()
    orders = Order.objects.filter(seller_id=seller, status="ordered")
    orderss = Order.objects.filter(seller_id=seller, status="ordered").count()

    context = {"reviews":reviews, "orders":orders, "orderss":orderss}
    return render(request, "user_templates/active_orders.html", context)


def manage_all_orders(request):

    user = request.user.id
    seller = Seller.objects.get(admin = user)
    reviews = Reviews.objects.filter(seller_id = seller.id).count()
    orders = Order.objects.filter(seller_id=seller)
    orderss = Order.objects.filter(seller_id=seller).count()

    context = {"reviews":reviews, "orders":orders, "orderss":orderss}
    return render(request, "user_templates/manage_orders.html", context)


def reject_order(request, order_id):

    try:
        order = Order.objects.get(id = order_id, status = "ordered")
        order.status = "rejected"
        order.save()
        return redirect(request.META.get("HTTP_REFERER"))

    except:
        return redirect(request.META.get("HTTP_REFERER"))


def post_request(request):

    if request.user.account_type == '3':
        user = request.user.id
        seller = Seller.objects.get(admin = user)
        reviews = Reviews.objects.filter(seller_id = seller.id).count()
        context = {"reviews":reviews}

    else:
        context = {}

    return render(request, "user_templates/post_request.html", context)


def post_request_save(request):
    if request.method == "POST":
        user = request.user.id
        charge = request.POST.get("charge")
        description = request.POST.get("description")

        try:
            user_id = customUser.objects.get(id = user)
            requests = Requests(poster = user_id, budget = charge, description = description)
            requests.save()
            messages.success(request, "Request Submission succesful")
            return redirect(request.META.get("HTTP_REFERER"))

        except:
            messages.error(request, "Request Submission Failed")
            return redirect(request.META.get("HTTP_REFERER"))

    return HttpResponse("Request cannot be processed")


def employer_requests(request):
    requestss = Requests.objects.all()
    requestsss = Requests.objects.all().count()

    if request.user.account_type == '3':
        user = request.user.id
        seller = Seller.objects.get(admin = user)
        reviews = Reviews.objects.filter(seller_id = seller.id).count()
        context = {"reviews":reviews, "requestsss":requestsss, "requestss":requestss}

    elif request.user.account_type == '2':
        context = {"requestsss":requestsss, "requestss":requestss}


    return render(request, "user_templates/employer_request.html", context)


@csrf_exempt
def reply_request_save(request):
    request_id = request.POST.get("request_id")
    message = request.POST.get("message")

    print(request_id)
    print(message)

    user = request.user.id
    seller = Seller.objects.get(admin = user)
    seller_id = seller.id

    try:
        reply = Request_replies(request_id = request_id, freelancer = seller, reply_text = message)
        reply.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def manage_requests(request):
    user = request.user.id
    requestss = Requests.objects.filter(poster = user)
    requestsss = Requests.objects.filter(poster = user).count()

    if request.user.account_type == '3':
        seller = Seller.objects.get(admin = user)    
        reviews = Reviews.objects.filter(seller_id = seller.id).count()

        paginate = Paginator(requestss, 3)
        p = request.GET.get("page")
        pages = paginate.get_page(p)

        context = {"requestss":requestss, "requestsss":requestsss, "reviews":reviews, "pages":pages}
    
    elif request.user.account_type == '2':

        paginate = Paginator(requestss, 3)
        p = request.GET.get("page")
        pages = paginate.get_page(p)

        context = {"requestss":requestss, "requestsss":requestsss, "pages":pages}

    return render(request, "user_templates/manage_requests.html", context)


def edit_request(request, request_id):
    reques = Requests.objects.get(id = request_id)
    if request.user.account_type == "3":
        user = request.user.id
        seller = Seller.objects.get(admin = user)
        reviews = Reviews.objects.filter(seller_id = seller.id).count()
        context = {"reviews":reviews, "reques":reques}

    elif request.user.account_type == "2":
        context = {"reques":reques}

    return render(request, "user_templates/edit_request.html", context)


def delete_request(request, request_id):
    reques = Requests.objects.get(id = request_id)
    reques.delete()

    return redirect(request.META.get("HTTP_REFERER"))


def edit_request_save(request):
    if request.method == "POST":
        description = request.POST.get("description")
        charge = request.POST.get("charge")
        request_id = request.POST.get("request_id")
        
        try:
            reques = Requests.objects.get(id = request_id)
            reques.description = description
            reques.budget = charge

            reques.save()
            messages.success(request, "Request Updated Successfully")
            return redirect(request.META.get("HTTP_REFERER"))

        except:
            messages.error(request, "Failed To Update Request")
            return redirect(request.META.get("HTTP_REFERER"))

    return HttpResponse("Request cannot be processed")


def view_replies(request, requessst_id):
    requestt_id = Requests.objects.get(id = requessst_id)
    if request.user.account_type == '3':
        user = request.user.id
        request_replies = Request_replies.objects.filter(request_id = requestt_id)
        seller_id = Seller.objects.get(admin = user)
        reviews = Reviews.objects.filter(seller_id = seller_id).count()
        request_repliesss = Request_replies.objects.filter(request_id = requestt_id).count()
        context = {"requestt_id":requestt_id, "reviews":reviews, "request_replies":request_replies, "request_repliesss":request_repliesss}
    
    elif request.user.account_type == '2':
        request_replies = Request_replies.objects.filter(request_id = requestt_id)
        request_repliesss = Request_replies.objects.filter(request_id = requestt_id).count()
        context = {"requestt_id":requestt_id, "request_replies":request_replies, "request_repliesss":request_repliesss}


    return render(request, "user_templates/view_replies.html", context)