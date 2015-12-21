from django import forms
from django.contrib import auth, messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
# from templated_email import send_templated_mail
from subscriber.models import ActivationCode
from django.contrib.sites.models import Site
import uuid
from md5 import md5
import datetime

from django.conf import settings

class RegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.save()
        
        activation_code = md5(str(uuid.uuid4())).hexdigest()
        try:
            ActivationCode.objects.get(code=activation_code)
        except Exception, e:
            ac = ActivationCode(code=activation_code)
            ac.user = user
            ac.status = 0
            ac.code_for = 0
            ac.save()

        current_site = Site.objects.get_current()
        if not settings.DEBUG:
            
            HOSTNAME = current_site.domain
            url = HOSTNAME+"/subscriber/registration/" + activation_code + "/active/"

            try:
                user.save()
                # send_templated_mail(
                #     template_name='registration_confirmation',
                #     from_email='hello@cloudcustomsolutions.com',
                #     recipient_list=[user.email,],
                #     context={
                #         'activation_url':url,
                #     },
                # )
                # ActivationCode.objects.create(user=user,code=activation_code, status=0)
                messages.add_message(self.request, messages.INFO, 'Please check your email for activation link.')
            except:
                messages.add_message(self.request, messages.INFO, 'Error in sending emails. Please contact the admin.')
        else:
            # user.is_active = True
            url = "http://127.0.0.1:8000"+"/subscriber/registration/" + activation_code + "/active/"
            try:
                testmail = send_mail("registration", url, "mamun1980@gmail.com", [user.email,], fail_silently=False)    
                messages.add_message(self.request, messages.INFO, 'Please check your email for activation link.')
            except Exception, e:
                messages.add_message(self.request, messages.INFO, 'Error in sending emails. Please contact the admin.')
            
            user.save()
        return user

class PasswordResetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)