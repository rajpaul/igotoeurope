from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from forms import RegistrationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.core import serializers
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from paypalrestsdk import Payment
import logging
import paypalrestsdk

# Create your views here.
from subscriber.models import *

def supplier_login(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            if user.is_active and user.is_staff:
                return HttpResponseRedirect("/superadmin/")
            elif user.is_active and not user.is_staff:
                try:
                    supplier = Supplier.objects.get(user=user)
                    redirect_url = supplier.get_profile_completion_status_redirect_url()
                except Supplier.DoesNotExist:
                    return HttpResponseRedirect("/subscriber/get-started/")
                return HttpResponseRedirect(redirect_url)
            else:
                messages.warning(request, "User %s not active yet" % (username))
                return HttpResponseRedirect("/")
        else:
            messages.warning(request, "User %s does not exits" % (username))
            return HttpResponseRedirect("/")
    else:
        return render(request, "subscriber/supplier-login.html", {})
@login_required
def supplier_logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect("/")
        else:
            return render(request, "subscriber/supplier-registration.html", {})            
    else:

        return render(request, "subscriber/supplier-registration.html", {})


def registration_active(request, activation_code):
    try:
        ac = ActivationCode.objects.get(code=activation_code, status=0, code_for=0)
        ac.status = 1
        ac.save()
        newuser = ac.user
        newuser.is_active = True
        newuser.save()
        return HttpResponseRedirect("/subscriber/"+str(newuser.id)+"/registration/success/")
    except Exception, e:
        ac = ActivationCode.objects.get(code=activation_code, code_for=0)
        if ac.is_expired:
            messages.add_message(request, messages.INFO, "Activation time is expired")
        elif ac.is_active:
            messages.add_message(request, messages.INFO, "Your account is inactive.")
        return HttpResponseRedirect("/")
    

def registration_success(request, uid):
    requested_user = User.objects.get(id=uid)
    requested_user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request, requested_user)
    try:
        supplier = Supplier.objects.get(user=requested_user)
        redirect_url = supplier.get_profile_completion_status_redirect_url()
    except Supplier.DoesNotExist:
        return HttpResponseRedirect("/supplier/get-started/")
    return HttpResponseRedirect(redirect_url)



@login_required
def get_started(request):
    # import pdb; pdb.set_trace();
    packages = Package.objects.filter(active=1).order_by("display_order")
    services = Service.objects.all()
    package_plans = PackagePlan.objects.all()
    frequencies = Frequency.objects.all()


    return render(request, "subscriber/get_started.html", 
        {'packages': packages, 'services': services, 'package_plans': package_plans, 
        'frequencies': frequencies})


def get_package_plan(request, ppid):
    pass
    

def get_coupon(request, code):
    try:
        coupon = CouponCode.objects.get(code=code)
        if coupon.expire_date > timezone.now() and coupon.status == '0':
            data = serializers.serialize("json", [coupon,]) 
            struct = json.loads(data)
            data = json.dumps(struct)
            return HttpResponse(data, content_type='application/json')
        elif coupon.expire_date < timezone.now():
            return HttpResponse("Expired")
        elif coupon.status == '1':
            return HttpResponse("Used")
        else:
            return HttpResponse("")
        
    except CouponCode.DoesNotExist:
        return HttpResponse("DoesNotExist")
        

@csrf_exempt
@login_required
def payment_create(request):
    #import pdb; pdb.set_trace();
    user = request.user
    plan_id = request.POST['ppid']
    plan_amount = request.POST['plan_amount']
    net_amount = request.POST['net_amount']
    coupon_code = request.POST['ccid']

    
    plan = PackagePlan.objects.get(pk=plan_id)
    if coupon_code != '0':
        cc = CouponCode.objects.get(pk=coupon_code)
    else:
        cc = None

    try:
        supplier, created = Supplier.objects.get_or_create(user=user)
        supplier.subscription_status = 0
        supplier.save()
    except Exception, e:
        raise e
    
    '''
    paypalrestsdk.configure({
        "mode": "sandbox", 
        "client_id": "AXD1xxBNG1VP1KO9j3PRAJmibtCGuNN7Zjry-5rIeE1UBZMjBEq6EqUiesOv",
        "client_secret": "EBINrBDb5Xl_jdkw2QeiwhLhN5TOZwFWQNOwhlbiyldIptJ8SxYtANUr3FHJ" 
    })
    site = request.META['HTTP_HOST']

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
        "return_url": "http://"+ site +"/payment/execute",
        "cancel_url": "http://"+ site +"/" },
        "transactions": [{
        "item_list": {
        "items": [{
            "name": plan.package.package_name,
            "sku": plan_id,
            "price": net_amount,
            "currency": "USD",
            "quantity": 1 }]},
            "amount": {
            "total": net_amount,
            "currency": "USD" },
            "description": "This is the payment transaction description." 
        }]
    })

    if payment.create():
        print("Payment[%s] created successfully" % (payment.id))
        ph = PaymentHistory(supplier=sp, plan=plan, plan_frequency=plan_frequesncy, plan_amount=plan_amount,
                   net_amount=net_amount)
        ph.payment_id = payment.id
        ph.payment_status = payment.state
        ph.payer_id = payment.create_time
        ph.create_time = payment.create_time
        
        # Redirect the user to given approval url
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = link.href
                query = parse_qs(urlparse(redirect_url).query)
                token = query['token'][0]
                ph.token = token
                ph.save()
        
        return redirect(redirect_url)
    else:
        print("Error while creating payment:")
        print(payment.error)
    
    return HttpResponse("Hello world!")
    return HttpResponseRedirect("/payment/error/")
    '''
    ph = PaymentHistory()
    ph.supplier = supplier
    ph.plan = plan
    if cc:
        ph.coupon = cc

    else:
        ph.coupon = None
    ph.plan_amount = plan_amount
    ph.net_amount = net_amount
    ph.token = '1232323232412'
    ph.save()
    return HttpResponseRedirect("/subscriber/payment/execute/")
    
@login_required
def payment_execute(request):
    sp = Supplier.objects.get(user=request.user)
    token = '1232323232412'
    ph = PaymentHistory.objects.get(token=token, supplier=sp)
    ph.payment_status = 'completed'
    ph.save()

    if ph.coupon:
        cs = CouponSupplier(coupon=ph.coupon, subscriber=sp.user, date_time=datetime.now())
        cs.save()

    subs = Subscription(user=sp.user, package_plan=ph.plan)
    subs.expire_date = datetime.now()+timedelta(days=int(ph.plan.frequency.duration_title))
    subs.plan_amount = ph.plan_amount
    subs.net_amount = ph.net_amount
    subs.subscription_status = 0
    subs.save()

    sp.subscription_status = 1
    sp.profile_completion_status = -1
    sp.save()

    return HttpResponseRedirect("/subscriber/payment/success/")

'''
    payer_id = request.GET['PayerID']
    token = request.GET['token']
    
    sp = Supplier.objects.get(supplier_user=request.user)
    ph = PaymentHistory.objects.get(token=token, supplier=sp)
    
    paypalrestsdk.configure({
        "mode": "sandbox", # sandbox or live
        "client_id": "AXD1xxBNG1VP1KO9j3PRAJmibtCGuNN7Zjry-5rIeE1UBZMjBEq6EqUiesOv",
        "client_secret": "EBINrBDb5Xl_jdkw2QeiwhLhN5TOZwFWQNOwhlbiyldIptJ8SxYtANUr3FHJ" 
    })
    
    payment = paypalrestsdk.Payment.find(ph.payment_id)
    
    if payment.execute({"payer_id": payer_id}):
        print("Payment execute successfully")
        ph.payment_status = 'completed'
        ph.save()
    else:
        print(payment.error) # Error Hash
    messages.success(request, 'Your payment is successfully loaded.')
    return HttpResponseRedirect("/ssm/buyer/")
'''

def payment_success(request):
    return HttpResponseRedirect("/supplier/search-corporation/")
