from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Address, AddressInfo, User, Profile
from utils.models import Misc


class AddressInfoInline(admin.StackedInline):
    model = AddressInfo
    extra = 0


class AddressAdmin(admin.ModelAdmin):
    inlines = [
        AddressInfoInline,
    ]
admin.site.register(Address, AddressAdmin)


class MiscAdmin(admin.ModelAdmin):
    list_display = ('item', 'name', 'value')
    fieldsets = (
        (None, {'fields': ('item', 'name', 'value')}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('item',)
        return self.readonly_fields
admin.site.register(Misc, MiscAdmin)


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'mobile')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    list_display = ('email', 'first_name', 'last_name', 'mobile', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'mobile')
    ordering = ('email',)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Profile)