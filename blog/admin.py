from django.contrib import admin

from blog.models import Blog

admin.site.register(Blog)

# @admin.register(Blog)
# class BlogAdmin(admin.ModelAdmin):
#     list_display = ('title', 'body', 'created_at',)
