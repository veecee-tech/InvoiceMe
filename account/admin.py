# from django.contrib import admin
# from .models import User
# # Register your models here.


# admin.site.register(User)

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserProfile

from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['account_number', 'is_admin']
    list_filter = ['is_admin', 'email', 'phone']
    fieldsets = (
        (None, {'fields': ('account_number', 'password')}),
        ('Personal info', {'fields': ('email','phone')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('account_number', 'password', 'password_2','is_staff','email', 'phone', 'is_admin', 'is_active')}
        ),
    )
    search_fields = ['account_number', 'email', 'phone']
    ordering = ['account_number']
    filter_horizontal = ()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','business_name', 'business_address', 'business_logo']

admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)