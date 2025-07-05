# my_real_estate_site/properties/models.py
from django.db import models
from django.utils.text import slugify

class PropertyType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Property(models.Model):
    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    description = models.TextField()
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True, related_name='properties')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=255) # e.g., "Douala, Bonamoussadi"
    address = models.CharField(max_length=255, blank=True, null=True)

    # Features
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    area_sqm = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True) # For built properties
    land_area_sqm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # For land listings

    # Status & Dates
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # Contact Info (optional, for specific property contacts)
    contact_person = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/') # Changed from ResizedImageField
    alt_text = models.CharField(max_length=255, blank=True)
    is_main = models.BooleanField(default=False) # To designate a main image

    def __str__(self):
        return f"Image for {self.property.title}"

class Service(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, help_text="e.g., A descriptive text for the icon")

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True) # e.g., "Villas", "Renovations"
    location = models.CharField(max_length=200, blank=True)
    completion_date = models.DateField(blank=True, null=True)
    main_image = models.ImageField(upload_to='projects/', blank=True, null=True) # Changed from ResizedImageField
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Inquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Inquiry from {self.name} about {self.property.title if self.property else 'General'}"