# my_real_estate_site/properties/admin.py
from django.contrib import admin
from .models import PropertyType, Property, PropertyImage, Service, Project, Inquiry

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'price', 'location', 'is_available', 'is_featured', 'published_date')
    list_filter = ('property_type', 'is_available', 'is_featured', 'location')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PropertyImageInline]
    date_hierarchy = 'published_date'
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'property_type', 'price', 'location', 'address')
        }),
        ('Features', {
            'fields': ('bedrooms', 'bathrooms', 'area_sqm', 'land_area_sqm')
        }),
        ('Status & Contact', {
            'fields': ('is_available', 'is_featured', 'contact_person', 'contact_phone', 'contact_email')
        }),
    )

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'completion_date', 'is_featured')
    list_filter = ('category', 'is_featured', 'location')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'property', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'message', 'property__title')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)