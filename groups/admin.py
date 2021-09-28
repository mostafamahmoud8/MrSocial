from django.contrib import admin
from .models import Group ,Membership
# Register your models here.

class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1

class GroupAdmin(admin.ModelAdmin):
    model=Group
    list_display = ['name','owner']
    inlines = (MembershipInline,)


admin.site.register(Group, GroupAdmin)