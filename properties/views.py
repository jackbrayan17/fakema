# my_real_estate_site/properties/views.py
from django.shortcuts import render, get_object_or_404
from .models import Property, Service, Project, Inquiry, PropertyType
from .forms import InquiryForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

def home_view(request):
    featured_properties = Property.objects.filter(is_featured=True, is_available=True)[:6]
    latest_properties = Property.objects.filter(is_available=True).order_by('-published_date')[:6]
    services = Service.objects.all()
    featured_projects = Project.objects.filter(is_featured=True)[:4]

    context = {
        'featured_properties': featured_properties,
        'latest_properties': latest_properties,
        'services': services,
        'featured_projects': featured_projects,
    }
    return render(request, 'properties/home.html', context)

def property_list_view(request):
    properties = Property.objects.filter(is_available=True)
    query = request.GET.get('q')
    property_type = request.GET.get('type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    bedrooms = request.GET.get('bedrooms')
    bathrooms = request.GET.get('bathrooms')

    if query:
        properties = properties.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(address__icontains=query)
        )
    if property_type:
        properties = properties.filter(property_type__name__iexact=property_type)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    if bedrooms:
        properties = properties.filter(bedrooms__gte=bedrooms)
    if bathrooms:
        properties = properties.filter(bathrooms__gte=bathrooms)

    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    property_types = PropertyType.objects.all()

    context = {
        'page_obj': page_obj,
        'property_types': property_types,
        'query_params': request.GET,
    }
    return render(request, 'properties/property_list.html', context)

def property_detail_view(request, slug):
    property = get_object_or_404(Property, slug=slug, is_available=True)
    images = property.images.all().order_by('-is_main')
    form = InquiryForm(request.POST or None, initial={'property': property})

    if request.method == 'POST':
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.property = property
            inquiry.save()
            messages.success(request, 'Your inquiry has been sent successfully!')
            return HttpResponseRedirect(reverse('properties:property_detail', args=[slug]))
        else:
            messages.error(request, 'There was an error sending your inquiry. Please check the form.')
    
    context = {
        'property': property,
        'images': images,
        'form': form,
    }
    return render(request, 'properties/property_detail.html', context)

def service_list_view(request):
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'properties/service_list.html', context)

def project_list_view(request):
    projects = Project.objects.all().order_by('-completion_date')
    paginator = Paginator(projects, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'properties/project_list.html', context)

def project_detail_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    context = {'project': project}
    return render(request, 'properties/project_detail.html', context)

def contact_view(request):
    form = InquiryForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully! We will get back to you shortly.')
            return HttpResponseRedirect(reverse('properties:contact'))
        else:
            messages.error(request, 'There was an error sending your message. Please check the form.')
    
    context = {'form': form}
    return render(request, 'properties/contact.html', context)

def about_view(request):
    return render(request, 'properties/about.html')