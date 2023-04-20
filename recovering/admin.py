import requests
from django.contrib import admin
from django.shortcuts import redirect

from .models import *


# Register your models here.

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_display = ['id', 'username', 'type', 'created']
    list_filter = ['type', 'created']
    ordering = ['type', 'created']


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        return redirect('/api/community/{}/'.format(object_id))


@admin.register(Comity)
class ComityAdmin(admin.ModelAdmin):
    search_fields = ['id', 'community']
    list_display = ['id', 'community']
    list_filter = ['id', 'community']
    ordering = ['community']


# admin.site.register(Community)
admin.site.register(Saloon)
admin.site.register(Version)
admin.site.register(Favorites)
admin.site.register(Message)
admin.site.register(FinalVersion)
admin.site.register(Admin)
