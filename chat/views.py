from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from chat.models import *
from core.models import *
from django.contrib.auth.decorators import login_required




@login_required
def room(request, room_name):
    if request.user.account_type == "2":
        receiver = customUser.objects.get(id = room_name)
        request.user.contacts.add(receiver.id)
        user_id = request.user.id
        userr = request.user.contacts
        user = Buyer.objects.get(admin = user_id)
        
        context = {"user":user,'userr':userr, 'receiver':receiver, "username":mark_safe(json.dumps(request.user.username)), "room_name_json":mark_safe(json.dumps(room_name))}

    if request.user.account_type == "3":
        receiver = customUser.objects.get(id = room_name)
        request.user.contacts.add(receiver.id)
        user_id = request.user.id
        user = Seller.objects.get(admin = user_id)
        userr = request.user.contacts
        context = {"user":user, 'receiver':receiver,'userr' :userr, "username":mark_safe(json.dumps(request.user.username)), "room_name_json":mark_safe(json.dumps(room_name))}
    return render(request, 'chat/room.html', context)