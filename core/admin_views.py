from django.shortcuts import *
from django.http import *
from core.models import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt



def smart_admin_home(request):
    return render(request, 'admin_templates/main_content.html', {})


def create_buyer(request):
    return render(request, "admin_templates/create_buyer.html", {})


def create_seller(request):
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    languages = Language.objects.all()
    levels = Xperienece_level.objects.all()
    labels = Label_choice.objects.all()

    return render(request, "admin_templates/create_seller.html", {"sub_categories":sub_categories, "categories":categories, "languages":languages, "levels":levels, "labels":labels,})


def create_category(request):
    return render(request, "admin_templates/create_category.html", {})


def create_sub_category(request):
    categories = Category.objects.all()
    return render(request, "admin_templates/create_sub_category.html", {"categories":categories})


def create_language(request):
    return render(request, "admin_templates/create_language.html", {})


def create_xperienece_level(request):
    return render(request, "admin_templates/create_xperienece_level.html", {})


def create_label_choice(request):
    return render(request, "admin_templates/create_label_choice.html", {})


def create_rating(request):
    return render(request, "admin_templates/create_stars.html", {})


def create_plan(request):
    return render(request, "admin_templates/create_plan.html", {})


def review_seller_admin(request):
    sellers = Seller.objects.all()
    ratings = star_rating.objects.all()
    return render(request, "admin_templates/review_seller_admin.html", {"sellers":sellers, "ratings":ratings})


def create_service_admin(request):
    sellers = Seller.objects.all()
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    plans = Plan.objects.all()
    return render(request, "admin_templates/create_service.html", {"sellers":sellers, "categories":categories, "sub_categories":sub_categories, "plans":plans})



def create_plan_save(request):
    if request.method == "POST":
        plan = request.POST.get('plan')

        try:
            plan = Plan(plan_name = plan)
            plan.save()
            messages.success(request, "Plan Created")
            return redirect("create_plan")

        except:
            messages.error(request, "Failed To Create Plan")
            return redirect("create_plan")
    
    return HttpResponse(" <h2> Invalid Request </h2>")



def create_seller_save(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        shortname = request.POST.get('short_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        language = request.POST.get('language')
        description = request.POST.get('description')
        gender = request.POST.get('gender')
        label = request.POST.get('label')
        level = request.POST.get('level')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        password = request.POST.get('password')
        profile_image = request.FILES['image']

        user = customUser.objects.filter(email = email).exists()

        fs = FileSystemStorage()
        profile_image_save = fs.save(profile_image.name, profile_image)
        image_url = fs.url(profile_image_save)

        cat_obj     = Category.objects.get(id = category)
        subcat_obj  = SubCategory.objects.get(id = subcategory)
        lang_obj    = Language.objects.get(id = language)
        level_obj   = Xperienece_level.objects.get(id = level)
        label_obj   = Label_choice.objects.get(id = label)

        if user:
            messages.error(request, "Failed To Create")
            return redirect("create_seller")

        try:

            user_seller = customUser.objects.create_user(username = username, email = email, password = password, account_type = 3)
            user_seller.seller.short_name = shortname
            user_seller.seller.address = address
            user_seller.seller.image = image_url
            user_seller.seller.description = description
            user_seller.seller.phone_number = phone
            user_seller.seller.gender = gender
            user_seller.seller.language = lang_obj
            user_seller.seller.experience_level = level_obj
            user_seller.seller.category = cat_obj
            user_seller.seller.sub_category = subcat_obj
            user_seller.seller.label = label_obj
            user_seller.save()
            
            messages.success(request, "Seller Account Created")
            return redirect("create_seller")

        except:
            messages.error(request, "Failed To Create")
            return redirect("create_seller")
    
    return HttpResponse(" <h2> Invalid Request </h2>")



def create_buyer_save(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        shortname = request.POST.get('short_name')
        password = request.POST.get('password')
        profile_image = request.FILES['image']

        user = customUser.objects.filter(email = email).exists()

        fs = FileSystemStorage()
        profile_image_save = fs.save(profile_image.name, profile_image)
        image_url = fs.url(profile_image_save)

        if user:
            messages.error(request, "Failed To Create")
            return redirect("create_buyer")

        try:
            user_buyer = customUser.objects.create_user(username = username, email = email, password = password, account_type = 2)
            user_buyer.buyer.short_name = shortname
            user_buyer.buyer.image = image_url
            user_buyer.save()

            messages.success(request, "Buyer Account Created")
            return redirect("create_buyer")

        except:
            messages.error(request, "Failed To Create")
            return redirect("create_buyer")
    
    return HttpResponse(" <h2> Invalid Request </h2>")



def create_xperienece_level_save(request):
    if request.method == "POST":
        level = request.POST.get('level')

        try:
            level = Xperienece_level(level = level)
            level.save()
            messages.success(request, "Level Created")
            return redirect("create_xperienece_level")

        except:
            messages.error(request, "Failed To Create")
            return redirect("create_xperienece_level")
    
    return HttpResponse(" <h2> Invalid Request </h2>")



def create_language_save(request):
    if request.method == "POST":
        language = request.POST.get('language')

        try:
            language = Language(language_name = language)
            language.save()
            messages.success(request, "Language Created")
            return redirect("create_language")

        except:
            messages.error(request, "Failed To Create")
            return redirect("create_language")
    
    return HttpResponse(" <h2> Invalid Request </h2>")



def create_label_choice_save(request):
    if request.method == "POST":
        label = request.POST.get('label')

        try:
            label = Label_choice(label = label)
            label.save()
            messages.success(request, "Label Created")
            return redirect("create_label_choice")

        except:
            messages.error(request, "Failed To Create")
            return redirect("create_label_choice")
    
    return HttpResponse(" <h2> Invalid Request </h2>")



def create_sub_category_save(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        title = request.POST.get('title')
        category_obj = Category.objects.get(id = category_id)

        try:
            sub_category = SubCategory(category = category_obj, sub_category_title = title)
            sub_category.save()
            messages.success(request, " Sub Category Created ")
            return redirect("create_sub_category")

        except:
            messages.error(request, " Failed To Create ")
            return redirect("create_sub_category")
    
    return HttpResponse(" <h2> Invalid Request </h2>")



def create_category_save(request):
    if request.method == "POST":
        title = request.POST.get('title')
        category_image = request.FILES['cat_image']

        fs = FileSystemStorage()
        category_image_save = fs.save(category_image.name, category_image)
        image_url = fs.url(category_image_save)

        try:
            category = Category(category_title = title, image = image_url)
            category.save()
            messages.success(request, " Category Created ")
            return redirect("create_category")

        except:
            messages.error(request, " Failed To Create")
            return redirect("create_category")
    
    return HttpResponse(" <h2> Invalid Request </h2>")



@csrf_exempt
def check_email(request):
    email = request.POST.get('email')
    user = customUser.objects.filter(email = email).exists()
    if user:
        return HttpResponse("True")
    return HttpResponse("False")




@csrf_exempt
def check_username(request):
    username = request.POST.get('username')
    user = customUser.objects.filter(username = username).exists()
    if user:
        return HttpResponse("True")
    return HttpResponse("False")



def create_service_admin_save(request):
    if request.method == "POST":
        seller_id = request.POST.get("seller_id")
        title = request.POST.get("title")
        charge = request.POST.get("charge")
        function = request.POST.get("function")
        cat_id = request.POST.get("cat_id")
        sub_cat_id = request.POST.get("sub_cat_id")
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
        
        cat_obj = Category.objects.get(id = cat_id)
        plan_obj = Plan.objects.get(id = plan)
        sub_cat_obj = SubCategory.objects.get(id = sub_cat_id)
        user= customUser.objects.get(id = seller_id)
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



def create_rating_save(request):
    if request.method == "POST":
        star = request.POST.get('rating')

        try:
            rating_save = star_rating(rating_star = star)
            rating_save.save()
            messages.success(request, "Rating Created Successfully")
            return redirect(request.META.get("HTTP_REFERER"))

        except:
            messages.error(request, "Failed To Create Rating")
            return redirect(request.META.get("HTTP_REFERER"))
    
    return HttpResponse('<h2> This process is not allowed </h2>')



def review_seller_admin_save(request):
    if request.method == "POST":
        seller_id = request.POST.get('seller_id')
        star_id = request.POST.get('star_id')
        content = request.POST.get('content')

        print("#######", star_id)

        user = customUser.objects.get(id = seller_id)
        seller_obj = Seller.objects.get(admin = user.id)
        star_obj = star_rating.objects.get(id = star_id)


        try:
            review = Reviews(seller_id = seller_obj, rating = star_obj, review_content = content)
            review.save()
            messages.success(request, "Review added success")
            return redirect(request.META.get("HTTP_REFERER"))

        except:
            messages.error(request, "Failed To Add Review")
            return redirect(request.META.get("HTTP_REFERER"))
    
    return HttpResponse('<h2> This process is not allowed </h2>')


