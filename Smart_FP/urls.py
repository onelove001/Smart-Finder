"""Smart_FP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import *
from core.user_views import *
from chat.views import *
from core.admin_views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name = 'landing_page'),
    path('login_user', login_user, name = 'login_user'),
    path('logout_user', logout_user, name = 'logout_user'),
    path('signup_user', signup_user, name = 'signup_user'),
    path('smart_admin', smart_admin_home, name = 'smart_admin_home'),
    path('smart_home', smart_home, name = 'smart_home'),

    # '============/ Admin Urls /========= ' #
    path('create_seller', create_seller, name = 'create_seller'),
    path('create_buyer', create_buyer, name = 'create_buyer'),
    path('create_category', create_category, name = 'create_category'),
    path('create_sub_category', create_sub_category, name = 'create_sub_category'),
    path('create_language', create_language, name = 'create_language'),
    path('create_xperienece_level', create_xperienece_level, name = 'create_xperienece_level'),
    path('create_label_choice', create_label_choice, name = 'create_label_choice'),
    path('create_service_admin', create_service_admin, name = 'create_service_admin'),
    path('check_username', check_username, name = 'check_username'),
    path('check_email', check_email, name = 'check_email'),
    path('create_service_admin_save', create_service_admin_save, name = 'create_service_admin_save'),

    path('create_seller_save', create_seller_save, name = 'create_seller_save'),
    path('create_buyer_save', create_buyer_save, name = 'create_buyer_save'),
    path('create_category_save', create_category_save, name = 'create_category_save'),
    path('create_sub_category_save', create_sub_category_save, name = 'create_sub_category_save'),
    path('create_language_save', create_language_save, name = 'create_language_save'),
    path('create_xperienece_level_save', create_xperienece_level_save, name = 'create_xperienece_level_save'),
    path('create_label_choice_save', create_label_choice_save, name = 'create_label_choice_save'),
    path('create_plan', create_plan, name = 'create_plan'),
    path('create_plan_save', create_plan_save, name = 'create_plan_save'),

    # =================/ User Urls /=============== #
    path('seller_page', seller_page, name = 'seller_page'),
    path('user_profile', user_profile, name = 'user_profile'),
    path('become_seller', become_seller, name = 'become_seller'),
    path('become_seller_save', become_seller_save, name = 'become_seller_save'),
    path('update_profile_seller', update_profile_seller, name = 'update_profile_seller'),
    path('update_profile_seller_save', update_profile_seller_save, name = 'update_profile_seller_save'),
    path('update_profile_buyer', update_profile_buyer, name = 'update_profile_buyer'),
    path('update_profile_buyer_save', update_profile_buyer_save, name = 'update_profile_buyer_save'),
    path('create_service_', create_service_, name = 'create_service_service'),
    path('create_service_save', create_service_save, name = 'create_service_save'),
    path('seller_profile_detail/<str:service_id>', seller_profile_detail, name = 'seller_profile_detail'),
    path('fetch_subcategories', fetch_subcategories, name = 'fetch_subcategories'),
    path('get_category/<str:category_id>', get_category, name = 'get_category'),
    path('search', search, name = 'search'),

    # =================/ Chat Urls /=============== #
    # path('chat', chat_index, name = "chat_index"),
    path('chat/<str:room_name>', room, name = "room_index"),
    
]


urlpatterns+=static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)