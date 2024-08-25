from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .forms import ContactForm, ProductModelForm
from django.contrib import messages
from .models import Product, Service, Team
from django.shortcuts import redirect
from django.views.generic import FormView
from django.urls import reverse_lazy

class IndexView(FormView):
    template_name = 'index.html'
    form_class = ContactForm
    success_url = reverse_lazy('index')
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = ContactForm()
        context['services'] = Service.objects.order_by('?').all()
        context['teams'] = Team.objects.order_by('?').all()
        return context
    
    def form_valid(self, form, *args, **kwargs):
        form.send_mail()
        messages.success(self.request, 'Email Sent Successfully')
        return super(IndexView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Email Send Fail')
        return super(IndexView, self).form_invalid(form, *args, **kwargs)

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
    if str(request.user) == 'AnonymousUser':
        return redirect('index')
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
