from django.contrib import admin


# from .models import Thread, ChatMessage

class ChatMessage(admin.TabularInline):
    pass
    # model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    pass
    # inlines = [ChatMessage]
    # class Meta:
    #     model = Thread 


# admin.site.register(Thread, ThreadAdmin)
