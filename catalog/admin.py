from django.contrib import admin

from .models import Category, Product, Manufacturer, SubCategory
from .forms import ProductAdminForm


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    list_display = ('name', 'price', 'discount_price', 'created', 'updated',)
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['-created']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created', 'updated',)
    prepopulated_fields = {'slug': ('name', 'dosage')}

admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created', 'updated',)
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Category, CategoryAdmin)


class ManufacturerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Manufacturer, ManufacturerAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
admin.site.register(SubCategory, SubCategoryAdmin)
