from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin



class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, *view_args, **view_kwargs):

        module_name = view_func.__module__
        print(module_name)
        user = request.user
        if user.is_authenticated:
            
            if user.account_type == "1":
                if module_name == "core.admin_views":
                    pass
                elif module_name == "core.views" or module_name == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("smart_admin_home"))


            elif user.account_type == "2":
                if module_name == "core.user_views":
                    pass
                elif module_name == "core.views" or module_name == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("smart_home"))


            elif user.account_type == "3":
                if module_name == "core.user_views":
                    pass
                elif module_name == "core.views" or module_name == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("smart_home"))
            else:
                return HttpResponseRedirect(reverse("landing_page"))
                   

        else:
            if request.path == reverse("landing_page") or request.path == reverse("login_user")  or module_name == "django.contrib.auth.views" or module_name == "core.views" or module_name == "core.admin_views" or module_name == "django.views.static":
                pass
            else:
                return HttpResponseRedirect(reverse("landing_page"))