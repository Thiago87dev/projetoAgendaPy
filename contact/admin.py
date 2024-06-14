from django.contrib import admin
from contact import models

# Register your models here.
@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = 'id', 'first_name', 'last_name', 'phone', 'show',
    ordering = '-created_date',
    list_filter = 'created_date',
    search_fields = 'id', 'first_name','last_name', 'phone',
    list_per_page = 20
    list_max_show_all = 350
    list_editable = 'show',
    list_display_links = 'id', 'first_name'


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name',
    ordering = '-id',