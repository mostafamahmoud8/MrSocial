from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,FriendShip,Block
from groups.admin import MembershipInline
from posts.admin import  CommentsInline,LikessInline,SharesInline


class FriedShipsInline(admin.TabularInline):
    model = FriendShip
    fk_name = "source"
    extra = 1

class BlockedInline(admin.TabularInline):
    model = Block
    fk_name = "source"
    extra = 1

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email','username','is_staff', 'is_active',)
    list_filter = ('email','username','is_staff', 'is_active',)
    fieldsets = (
        ('Authentication Information', {'fields': ('email','username','password')}),
        ('Personal Information',{'fields':('first_name','last_name','birth_date')}),
        ('Profile Picture',{'fields':('image',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username','password1', 'password2','first_name','last_name','birth_date','image','is_staff', 'is_active','is_superuser')}
        ),
    )
    search_fields = ('email','useranme')
    ordering = ('email','username')
    inlines = (MembershipInline,FriedShipsInline,BlockedInline,CommentsInline,LikessInline,SharesInline,)


admin.site.register(CustomUser, CustomUserAdmin)