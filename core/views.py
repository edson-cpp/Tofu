from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .forms import ContactForm, ProductModelForm
from django.contrib import messages
from .models import Product

def index(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'index.html', context)

def contact(request):
    form = ContactForm(request.POST or None)
    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail()
            messages.success(request, 'Email Sent Successfully')
            form = ContactForm()
        else:
            messages.error(request, 'Email Send Fail')

    context = {
        'form': form
    }
    return render(request, 'contact.html', context)

def product(request):
    if str(request.method) == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product saved successfully!')
            form = ProductModelForm()
        else:
            messages.error(request, 'Error saving product!')
    else:
        form = ProductModelForm()
    context = {
        'form': form
    }
    return render(request, 'product.html', context)
