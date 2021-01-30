from django.db import models
from django.contrib.auth.models import *
from django.utils import timezone


Gender = (

    ("male", "male"),
    ("female", "female"),

)


order_ser = (

    ("not_ordered", "not_ordered"),
    ("ordered", "ordered"),
    ("delivered", "delivered"),
)



order_service = (

    ("ordered", "ordered"),
    ("delivered", "delivered"),
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



class Category(models.Model):

    id                  = models.AutoField(primary_key=True)
    category_title      = models.CharField(max_length = 50)
    image               = models.FileField()
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
    created             = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.admin.email} - seller"

    



class Plan(models.Model):

    id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length = 20)

    def __str__(self):
        return f"{self.plan_name}"


class Service(models.Model):

    id                  = models.AutoField(primary_key=True)
    owner               = models.ForeignKey(Seller, on_delete = models.CASCADE)
    title               = models.CharField(max_length = 100)
    orders              = models.ForeignKey("Order", on_delete = models.SET_NULL, null = True)
    ordered             = models.CharField(choices = order_ser, max_length=20, default = "not_ordered")
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
        return f"{self.owner.admin.username} - {self.owner.category.category_title}"

    def cat_count(self):
        return self.category.all().count()


    def get_number_orders(self):
        return self.order_set.all().count()



class star_rating(models.Model):
    id = models.AutoField(primary_key = True)
    rating_star = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.rating_star}"



class Reviews(models.Model):
    id = models.AutoField(primary_key = True)
    seller_id = models.ForeignKey(Seller, on_delete = models.CASCADE)
    rating = models.ForeignKey(star_rating, on_delete = models.SET_NULL, null = True)
    review_content = models.TextField()

    def __str__(self):
        return f"{self.rating} stars - for - {self.seller_id.admin.username}"



class Order(models.Model):

    id = models.AutoField(primary_key = True)
    user_order = models.ForeignKey(customUser, on_delete = models.CASCADE)
    service_ordered = models.ForeignKey(Service, on_delete = models.CASCADE)
    status = models.CharField(choices=order_service, max_length = 20)
    date_ordered = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.user_order.username} {self.status}"
