from django.contrib import admin

from client.models import ServiceClient, Message, Newsletter, Logi


@admin.register(ServiceClient)
class ServiceClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('topic', 'message',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'status', 'owner')


admin.site.register(Logi)
# @admin.register(Logi)
# class LogiAdmin(admin.ModelAdmin):
#     list_display = ('last', 'settings',)
