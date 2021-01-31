from django.contrib import admin
from core.models import *
from django.contrib.auth.admin import UserAdmin




class UserModel(UserAdmin):
    pass



admin.site.register(customUser, UserModel)
admin.site.register(Buyer)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Language)
admin.site.register(Xperienece_level)
admin.site.register(Label_choice)
admin.site.register(Seller)
admin.site.register(Service)
admin.site.register(star_rating)
admin.site.register(Reviews)
admin.site.register(order)

