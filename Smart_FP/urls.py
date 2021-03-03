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
from django.urls import path, include, re_path
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
    path('search22', search22, name = 'search22'),
    path('search_result/<str:search_id>', search_result, name = 'search_result'),



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
    path('create_delivery_days', create_delivery_days, name = 'create_delivery_days'),
    path('create_delivery_save', create_delivery_save, name = 'create_delivery_save'),
    path('create_label_choice_save', create_label_choice_save, name = 'create_label_choice_save'),
    path('create_plan', create_plan, name = 'create_plan'),
    path('create_plan_save', create_plan_save, name = 'create_plan_save'),
    path('create_rating', create_rating, name = 'create_rating'),
    path('create_rating_save', create_rating_save, name = 'create_rating_save'),
    path('review_seller_admin', review_seller_admin, name = 'review_seller_admin'),
    path('review_seller_admin_save', review_seller_admin_save, name = 'review_seller_admin_save'),



    # =================/ User Urls /=============== #
    path('dashboard', user_profile, name = 'user_profile'),
    path('become_seller', become_seller, name = 'become_seller'),
    path('become_seller_save', become_seller_save, name = 'become_seller_save'),
    path('update_profile_seller', update_profile_seller, name = 'update_profile_seller'),
    path('update_profile_seller_save', update_profile_seller_save, name = 'update_profile_seller_save'),
    path('update_profile_buyer', update_profile_buyer, name = 'update_profile_buyer'),
    path('update_profile_buyer_save', update_profile_buyer_save, name = 'update_profile_buyer_save'),
    path('create_service_', create_service_, name = 'create_service_service'),
    path('create_service_save', create_service_save, name = 'create_service_save'),
    path('service_detail/<str:service_id>', service_detail, name = 'service_detail'),
    path('fetch_subcategories', fetch_subcategories, name = 'fetch_subcategories'),
    path('occupation/<str:category_id>', get_category, name = 'get_category'),
    path('search', search, name = 'search'),
    path('user_review_save', user_review_save, name = 'user_review_save'),
    path('user_service_order', user_service_order, name = 'user_service_order'),
    path('freelancers_page/<str:category_idd>', freelancers_page, name = 'freelancers_page'),
    path('seller_profile/<str:seller_id>', seller_profile, name = 'seller_profile'),
    path('edit_service/<str:service_edit_id>', edit_service, name = 'edit_service'),
    path('delete_service/<str:service_delete_id>', delete_service, name = 'delete_service'),
    path('seller_reviews', seller_reviews, name = 'seller_reviews'),
    path('manage_services', manage_services, name = 'manage_services'),
    path('edit_service_save', edit_service_save, name = 'edit_service_save'),
    path('manage_all_orders', manage_all_orders, name = 'manage_all_orders'),
    path('active_orders', active_orders, name = 'active_orders'),
    path('buyer_profile/<str:buyer_id>', buyer_profile, name = 'buyer_profile'),
    path('reject_order/<str:order_id>', reject_order, name = 'reject_order'),
    path('post_request', post_request, name = 'post_request'),
    path('post_request_save', post_request_save, name = 'post_request_save'),
    path('employer_requests', employer_requests, name = 'employer_requests'),
    path('reply_request_save', reply_request_save, name = 'reply_request_save'),
    path('manage_requests', manage_requests, name = 'manage_requests'),
    path('edit_request/<str:request_id>', edit_request, name = 'edit_request'),
    path('edit_request_save', edit_request_save, name = 'edit_request_save'),
    path('delete_request/<str:request_id>', delete_request, name = 'delete_request'),
    path('view_replies/<str:requessst_id>', view_replies, name = 'view_replies'),
    path('reply_request/<str:request_id>', reply_request, name = 'reply_request'),
    path('page_404', page_404, name = 'page_404'),
    path('contact_us', contact_us_page, name = 'contact_us_page'),
    path('contact_us_save', contact_us_save, name = 'contact_us_save'),
    path('see_reviews', see_reviews, name = 'see_reviews'),
    path('ordered_listing', ordered_listing, name = 'ordered_listing'),
    path('mark_as_deliver/<str:order_id>', mark_as_deliver, name = 'mark_as_deliver'),
    path('proceed_payment/<str:order_id>', proceed_payment, name = 'proceed_payment'),
    path('payment_invoice/<str:order_id>', payment_invoice, name = 'payment_invoice'),
    path('payment_confirmation/<str:order_id>', payment_confirmation, name = 'payment_confirmation'),
    path('news_letter_save', news_letter_save, name = 'news_letter_save'),
    path('wallet', wallet, name = 'wallet'),
    path('blog', blog, name = 'blog'),
    path('save_skills', save_skills, name = 'save_skills'),
    path('add_skills', add_skills, name = 'add_skills'),
    path('add_skills_service/<str:service_id>', add_skills_service, name = 'add_skills_service'),
    path('add_skills_service_save', add_skills_service_save, name = 'add_skills_service_save'),
    
    



    # =================/ Chat Urls /=============== #
    # path('messages', InboxView.as_view(), name = "inbox_messages"),
    path('messages', messages_view, name = "messages_view"),
    re_path(r"^messages/(?P<username>[\w.@+-]+)/", ThreadView.as_view(), name = "thread"),
    
]


urlpatterns+=static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)