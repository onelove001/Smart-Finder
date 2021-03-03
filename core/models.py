from django.db import models
from django.contrib.auth.models import *
from django.utils import timezone
from PIL import Image


Gender = (

    ("male", "male"),
    ("female", "female"),

)


Verified = (

    ("yes", "yes"),
    ("no", "no"),

)


order_service = (
    ("ordered", "ordered"),
    ("paid", "paid"),
    ("delivered", "delivered"),
    ("rejected", "rejected"),
)


class customUser(AbstractUser):

    accout_choices      = ( (1, "Admin"), (2, "Buyer"), (3, "Seller"), )
    account_type        = models.CharField(max_length = 9, choices = accout_choices, default = 1)
    contacts            = models.ManyToManyField('self', blank = True)
   
    
    def return_seller_image(self):
        return self.seller.image

    def return_buyer_image(self):
        return self.buyer.image



class Admin(models.Model):

    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(customUser, on_delete = models.CASCADE)
    created = models.DateTimeField(default = timezone.now)
    updated = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.admin.account_type}"



class Buyer(models.Model):

    id = models.AutoField(primary_key=True)
    admin           = models.OneToOneField(customUser, on_delete = models.CASCADE)
    short_name      = models.CharField(max_length = 20)
    image           = models.FileField()
    created         = models.DateTimeField(default = timezone.now)    

    def __str__(self):
        return f"{self.admin.email} - buyer"

    def return_time(self):
        return self.created.strftime("%d/%m/%Y")



class Category(models.Model):

    id                  = models.AutoField(primary_key=True)
    category_title      = models.CharField(max_length = 50)
    image               = models.FileField()
    category_words      = models.CharField(max_length = 50)
    seller              = models.ForeignKey("Seller", on_delete = models.SET_NULL, null = True, related_name="sellerss")

    def __str__(self):
        return self.category_title

    def get_number_of_sellers(self):
        return self.sell.all().count()

    def get_number_of_services(self):
        return self.service_set.all().count()



class SubCategory(models.Model):

    id = models.AutoField(primary_key = True)
    category                    = models.ForeignKey(Category, on_delete = models.CASCADE)
    sub_category_title          = models.CharField(max_length = 50)

    def __str__(self):
        return f"{self.sub_category_title}"

    objects = models.Manager()



class Language(models.Model):

    id = models.AutoField(primary_key = True)
    language_name = models.CharField(max_length = 50)

    def __str__(self):
        return f"{self.language_name}"



class Xperienece_level(models.Model):

    id      = models.AutoField(primary_key = True)
    level   = models.CharField(max_length = 50)

    def __str__(self):
        return f"{self.level}"



class Label_choice(models.Model):

    id      = models.AutoField(primary_key = True)
    label   = models.CharField(max_length = 50)

    def __str__(self):
        return f"{self.label}"



class Seller(models.Model):

    id = models.AutoField(primary_key=True)
    admin               = models.OneToOneField(customUser, on_delete = models.CASCADE)
    short_name          = models.CharField(max_length = 20)
    phone_number        = models.CharField(max_length = 20)
    address             = models.CharField(max_length = 100)
    gender              = models.CharField(max_length = 10, choices=Gender, default = 1)
    image               = models.FileField()
    description         = models.TextField()
    language            = models.ForeignKey(Language, on_delete = models.SET_NULL, null = True)
    experience_level    = models.ForeignKey(Xperienece_level, on_delete = models.SET_NULL, null = True)
    category            = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True, related_name="sell")
    sub_category        = models.ForeignKey(SubCategory, on_delete = models.SET_NULL, null = True)
    label               = models.ForeignKey(Label_choice, on_delete = models.SET_NULL, null = True)
    verified            = models.CharField(choices=Verified, default="no", max_length=10)
    created             = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.admin.email} - seller"


    def return_time(self):
        return self.created.strftime("%d/%m/%Y")



class Plan(models.Model):

    id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length = 20)

    def __str__(self):
        return f"{self.plan_name}"



class Delivery_days(models.Model):
    id = models.AutoField(primary_key=True)
    days = models.IntegerField()

    def __str__(self):
        return f"{self.days} days"



class Service(models.Model):

    id                  = models.AutoField(primary_key=True)
    owner               = models.ForeignKey(Seller, on_delete = models.CASCADE)
    title               = models.CharField(max_length = 100)
    days                = models.ForeignKey(Delivery_days, on_delete = models.SET_NULL, null = True)
    orders              = models.ForeignKey("Order", on_delete = models.SET_NULL, null = True)
    category            = models.ForeignKey(Category, on_delete = models.CASCADE)
    sub_category        = models.ForeignKey(SubCategory, on_delete = models.SET_NULL, null = True)
    plan                = models.ForeignKey(Plan, on_delete = models.SET_NULL, null = True)
    charge              = models.FloatField()
    description         = models.TextField()
    function            = models.TextField()
    image1              = models.FileField() 
    image2              = models.FileField()
    image3              = models.FileField()
    created             = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.owner.admin.username} - {self.owner.category.category_title} - {self.title}"


    def cat_count(self):
        return self.category.all().count()


    def get_number_orders(self):
        return self.order_set.all().filter(status = "ordered").count()



class Added_skills(models.Model):
    id = models.AutoField(primary_key = True)
    seller = models.ForeignKey(Seller, on_delete = models.CASCADE)
    skill_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.seller.admin.username} {self.skill_name}"



class Added_skills_service(models.Model):
    id = models.AutoField(primary_key = True)
    service = models.ForeignKey(Service, on_delete = models.CASCADE)
    skill_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.service.title} - {self.skill_name}"



class star_rating(models.Model):
    id = models.AutoField(primary_key = True)
    rating_star = models.IntegerField()

    def __str__(self):
        return f"{self.rating_star}"



class Reviews(models.Model):
    id = models.AutoField(primary_key = True)
    user_id = models.ForeignKey(customUser, on_delete = models.SET_NULL, null = True)
    seller_id = models.ForeignKey(Seller, on_delete = models.SET_NULL, null = True)
    service_id = models.ForeignKey(Service, on_delete = models.SET_NULL, null = True)
    rating = models.ForeignKey(star_rating, on_delete = models.SET_NULL, null = True)
    review_content = models.TextField()
    date_reviewed = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.user_id.username} left {self.rating} stars for {self.seller_id.admin.username}"



class Order(models.Model):

    id = models.AutoField(primary_key = True)
    user_order = models.ForeignKey(customUser, on_delete = models.CASCADE)
    seller_id = models.ForeignKey(Seller, on_delete = models.CASCADE, null = True)
    service_ordered = models.ForeignKey(Service, on_delete = models.CASCADE)
    status = models.CharField(choices=order_service, max_length = 20)
    date_ordered = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.user_order.username} {self.status}"



class Requests(models.Model):
    id = models.AutoField(primary_key=True)
    poster = models.ForeignKey(customUser, on_delete=models.CASCADE)
    budget = models.IntegerField()
    description = models.TextField()
    created = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.poster.username



class Request_replies(models.Model):
    id = models.AutoField(primary_key=True)
    request_id = models.ForeignKey(Requests, on_delete = models.CASCADE)
    freelancer = models.ForeignKey(Seller, on_delete = models.CASCADE)
    reply_text = models.TextField()
    created = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.freelancer} replied {self.request_id.poster.username}"  



class Contact_Us(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.TextField(max_length=30)

    def __str__(self):
        return self.email



class NewsLetter(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()



class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Seller, on_delete = models.CASCADE)
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    wallet_acc = models.FloatField(default = 0)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"hey {self.user.admin.username}, {self.order.user_order.username} Paid For {self.order.service_ordered.title}"

    def get_vat(self):
        vat = (20/100 * (self.order.service_ordered.charge))
        return vat



class Reply_notifications(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(customUser, on_delete = models.CASCADE)
    request_replies  = models.ForeignKey(Request_replies, models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.request_replies.freelancer.admin.username} replied {self.user.username}"

    def get_first_words(self):
        return f"{self.request_replies.request_id.description[:20]}"



class Review_notifications(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Seller, on_delete = models.CASCADE)
    review  = models.ForeignKey(Reviews, models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.review.user_id.username} sent a review"



class Order_notifications(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Seller, on_delete = models.CASCADE)
    order  = models.ForeignKey(Order, models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.order.user_order.username} {self.order.status} your {self.order.service_ordered.title}"

   