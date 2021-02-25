from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import *
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from .forms import ComposeForm
from django.urls import reverse_lazy
from chat.models import *
from core.models import *
from django.contrib.auth.decorators import login_required



@login_required
def messages_view(request):

    user = request.user.id
    userrr = request.user.username
    userr = request.user
    users = Thread.objects.get_all_users(userrr)
    print("users", users)
    requestsssss = Requests.objects.all().count() 
    reply_notifications = Reply_notifications.objects.filter(user = user)
    notifications = Reply_notifications.objects.filter(user = user).count()

    if request.user.account_type == "3":
        seller = Seller.objects.get(admin = user)
        reviews = Reviews.objects.filter(seller_id = seller.id).count()
        requestsssss = Requests.objects.all().count()
        order_notifications = Order_notifications.objects.filter(user = userr.seller.id)
        notifications2 = Order_notifications.objects.filter(user = userr.seller.id).count()
        review_notifications = Review_notifications.objects.filter(user = userr.seller.id)
        notifications3 = Review_notifications.objects.filter(user = userr.seller.id).count()
        notificationsss = notifications + notifications2 + notifications3
        context = {

            "users":users,
            "reviews":reviews,
            "requestsssss":requestsssss,
            "reply_notifications":reply_notifications,
            "notifications":notifications,
            "order_notifications":order_notifications,
            "notifications2":notifications2,
            "notificationsss":notificationsss,
            "review_notifications":review_notifications,
            "notifications3":notifications3,
        }

    elif request.user.account_type == "2":
        usersss = customUser.objects.filter(account_type = '3')
        context = {
            "users":usersss,
            "requestsssss":requestsssss,
            "reply_notifications":reply_notifications,
            "notifications":notifications,
        }

    return render(request, "chat/messages.html", context)


class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/messages_id.html'
    form_class = ComposeForm

    def get_success_url(self, **kwargs):
        other_username  = self.kwargs.get("username")
        return reverse("thread", kwargs = {"username":other_username})
        
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = self.request.user.id
        # userr = self.request.user
        # reply_notifications = Reply_notifications.objects.filter(user = user)
        # notifications = Reply_notifications.objects.filter(user = user).count()
        # requestsssss = Requests.objects.all().count()

        # if self.request.user.account_type == "3":
        #     seller = Seller.objects.get(admin = user)
        #     reviews = Reviews.objects.filter(seller_id = seller.id).count()
        #     order_notifications = Order_notifications.objects.filter(user = userr.seller.id)
        #     notifications2 = Order_notifications.objects.filter(user = userr.seller.id).count()
        #     review_notifications = Review_notifications.objects.filter(user = userr.seller.id)
        #     notifications3 = Review_notifications.objects.filter(user = userr.seller.id).count()
        #     notificationsss = notifications + notifications2 + notifications3

        #     context = {
        #         # "form":self.get_form(),
        #         "requestsssss":requestsssss,
        #         "reply_notifications":reply_notifications,
        #         "notifications":notifications,
        #         "order_notifications":order_notifications,
        #         "notifications2":notifications2,
        #         "notificationsss":notificationsss,
        #         "review_notifications":review_notifications,
        #         "notifications3":notifications3,
        #         "reviews":reviews,
        #     }

        # else:
        #     context = {
        #         # "form":self.get_form(),
        #         "requestsssss":requestsssss,
        #         "reply_notifications":reply_notifications,
        #         "notifications":notifications,
                
        #     }

        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)


