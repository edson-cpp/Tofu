from django import forms
from django.core.mail.message import EmailMessage
from .models import Product

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='E-mail', max_length=100)
    subject = forms.CharField(label='Subject', max_length=150)
    message = forms.CharField(label='Message', widget=forms.Textarea())

    def send_mail(self):
        sm_name = self.cleaned_data['name']
        sm_email = self.cleaned_data['email']
        sm_subject = self.cleaned_data['subject']
        sm_message = self.cleaned_data['message']

        content = f'Name: {sm_name}\nEmail: {sm_email}\nSubject: {sm_subject}\nMessage: {sm_message}'
        mail = EmailMessage(
            subject=sm_subject,
            body=content,
            from_email='contact@yourdomain.com',
            to=['contact@yourdomain.com',],
            headers={'Reply-To': sm_email}
        )
        mail.send()

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image']