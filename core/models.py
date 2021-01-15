from django.db import models
from django.contrib.auth.models import *
from django.utils import timezone



Gender = (

    ("male", "male"),
    ("female", "female"),

)


class customUser(AbstractUser):
    accout_choices      = ( (1, "Admin"), (2, "Buyer"), (3, "Seller"), )
    account_type        = models.CharField(max_length = 9, choices = accout_choices, default = 1)
    contacts            = models.ManyToManyField('self', blank = True)
    Buyer               = models.ForeignKey('Buyer', on_delete = models.SET_NULL, null = True)
    Seller              = models.ForeignKey('Seller', on_delete = models.SET_NULL, null = True)
    


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

    def __str__(self):
        return self.category_title



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
    language            = models.ForeignKey(Language, on_delete = models.CASCADE, null = True)
    experience_level    = models.ForeignKey(Xperienece_level, on_delete = models.CASCADE, null = True)
    category            = models.ForeignKey(Category, on_delete = models.CASCADE, null = True)
    sub_category        = models.ForeignKey(SubCategory, on_delete = models.CASCADE, null = True)
    label               = models.ForeignKey(Label_choice, on_delete = models.CASCADE, null = True)
    created             = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.admin.email} - seller"



class Plan(models.Model):
    plan_name = models.CharField(max_length = 20)

    def __str__(self):
        return f"{self.plan_name}"


class Service(models.Model):

    id                  = models.AutoField(primary_key=True)
    owner               = models.ForeignKey(Seller, on_delete = models.CASCADE)
    title               = models.CharField(max_length = 100)
    category            = models.ForeignKey(Category, on_delete = models.CASCADE, null = True)
    sub_category        = models.ForeignKey(SubCategory, on_delete = models.CASCADE, null = True)
    plan                = models.ForeignKey(Plan, on_delete = models.CASCADE, null = True)
    charge              = models.FloatField()
    description         = models.TextField()
    function            = models.TextField()
    image1              = models.FileField() 
    image2              = models.FileField()
    image3              = models.FileField()
    created             = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.owner.admin.username} - {self.owner.category.category_title}"



# class Reviews(models.Model):
#     id = models.AutoField(primary_key = True)
#     seller_id = models.ForeignKey(Seller, on_delete = models.CASCADE)
#     review_content = models.TextField()