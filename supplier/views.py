from django.shortcuts import render
from django.contrib import auth, messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from subscriber.models import *
from supplier.models import *
from supplier.forms import *
from supplier.choices import * 

from django.core import serializers
import json
from django.utils.timezone import utc
import datetime
# from supplier.models import Supplier
from haystack.forms import ModelSearchForm, SearchForm
from haystack.query import SearchQuerySet, EmptySearchQuerySet
from haystack.inputs import Raw, Clean, AutoQuery

def search_buyer(request):
    query = request.GET.get('q','')
    if request.GET.get('q'):
        buyers = SearchQuerySet().using('default').filter(content=AutoQuery(query)).load_all()[:10]
    else:
        buyers = SearchQuerySet().using('default').all().load_all()[:10]

    buyer_list = []
    if buyers:
        for buyer in buyers:
            if buyer != None:
                buyer_dict = {}
                buyer_dict['id'] = buyer.pk
                buyer_dict['company_name'] = buyer.company_name
                
                buyer_list.append(buyer_dict)

    the_data = json.dumps({
        'results': buyer_list
    })
    return HttpResponse(the_data, content_type='application/json')

def search_corporation(request):
    saved_buyers = []
    ps_categories = ProductAndServiceCategory.objects.all()
    sp = Supplier.objects.get(user=request.user)
    # ssubmissions = sp.suppliersubmission_set.all()
    ssb = SupplierSelectedBuyers.objects.filter(supplier=sp)

    if ssb:
        for ssubmission in ssb:
            saved_buyers.append(ssubmission.buyer)

    return render(request, "supplier/search_corporation.html", 
        {'categories': ps_categories, 'saved_buyers': saved_buyers})


@csrf_exempt
def search_buyers(request):
    saved_buyers = []
    buyers_list = []
    final_buyers_list = []
    sp = Supplier.objects.get(user=request.user)
    # ssubmissions = sp.suppliersubmission_set.all()
    ssb = SupplierSelectedBuyers.objects.filter(supplier=sp)

    if ssb:
        for ssubmission in ssb:
            saved_buyers.append(ssubmission.buyer)

    showall = request.POST['showall']

    if len(request.POST['findbuyer']) > 0:
        findbuyers = request.POST['findbuyer'].split(", ")
    else:
        findbuyers = None

    if len(request.POST['findcat']) > 0:
        findcats = request.POST['findcat'].split(", ")
    else:
        findcats = None

    #====== filtering buyers for categories ===========

    clist = []    
    if findcats:
        for cat in findcats:
            catq1 = ProductAndServiceCategory.objects.filter(category_name__contains=cat).distinct()
            for cq in catq1:
                clist.append(cq.pk)

    if len(request.POST['categories']) > 0:
        categories = request.POST['categories']

        cats = categories.split(", ")

        for cat in cats:
            #cid = cat.split("=")[1]
            clist.append(cat)
    
    buyers_from_cat = Buyer.objects.filter(product_service_category__in=clist).distinct()
    for br in buyers_from_cat:
        buyers_list.append(br)

    #====== filtering buyers for manual  input ===========
    no_buyer_found = []

    if findbuyers:
        for findbuyer in findbuyers:
            try:
                fbuyers = Buyer.objects.filter(company_name__contains=findbuyer).distinct()
                for fb in fbuyers:
                    if fb not in buyers_list:
                        buyers_list.append(fb)
            except (ValueError, Buyer.DoesNotExist):
                no_buyer_found.append(findbuyer)
    

    if showall == 'no':

        
        for bl in buyers_list:
            if bl not in saved_buyers:
                final_buyers_list.append(bl)
    else:
        final_buyers_list = buyers_list

    total_suppliers = Supplier.objects.count()

    return render(request, 'supplier/searched_buyers.html',
        {'buyers': final_buyers_list, 'saved_buyers':saved_buyers, 'no_buyer_found':no_buyer_found, "total_suppliers":total_suppliers })

@csrf_exempt
def save_buyers(request):
    # import pdb; pdb.set_trace()
    if len(request.POST['selectedbuyers']) > 0:

        #===== get all selected buyers============
        buyer_list = []
        buyers = request.POST['selectedbuyers']
        buyerslist = buyers.split("&")[1:]
        for br in buyerslist:
            bid = br.split("=")[1]
            buyerobj = Buyer.objects.get(pk=bid)
            buyer_list.append(buyerobj)

        #========= get supplier ===================
        
        sp = Supplier.objects.get(user=request.user)

        #========= get saved supplier if any ====== 
        saved_buyers = []        
        ssbs = SupplierSelectedBuyers.objects.filter(supplier=sp)
        if ssbs:
            for ssubmission in ssbs:
                saved_buyers.append(ssubmission.buyer)
        
        
        duplicate_buyers = []
        added_buyers = []
        sdate = datetime.datetime.utcnow().replace(tzinfo=utc)

        for buyer in buyer_list:
            
            if buyer not in saved_buyers:
                ssb = SupplierSelectedBuyers(supplier=sp, buyer=buyer)
                ssb.save()
                added_buyers.append(buyer)
            else:
                duplicate_buyers.append(buyer)
        
        saved_buyers = saved_buyers + added_buyers
        return render(request, 'supplier/selected_buyers.html',
                {'saved_buyers': saved_buyers, 'duplicate_buyers': duplicate_buyers})
        
    else:
        return HttpResponse('No')

@csrf_exempt
def delete_buyer(request):
    bid = request.POST['bid']
    buyer = Buyer.objects.get(pk=bid)
    usr = request.user
    sp = Supplier.objects.get(user=usr)
    ssb = SupplierSelectedBuyers.objects.get(supplier=sp, buyer=buyer)
    ssb.delete()
    return HttpResponse(bid)
    # saved_buyers = []        
    # ssubmissions = SupplierSelectedBuyers.objects.filter(supplier=sp, buyer=buyer)
    # if ssubmissions:
    #     for ssubmission in ssubmissions:
    #         saved_buyers.append(ssubmission.buyer)

    return render(request, 'supplier/selected_buyers.html',
                {'saved_buyers': saved_buyers})


def add_manual_buyer(request):
    pass

@login_required
def supplier_profile(request):
    
    salutations = SALUTATION
    user = request.user
    supplier, created = Supplier.objects.get_or_create(user=user)
    print created
    print supplier.profile_completion_status
    if created:
        supplier.profile_completion_status = -1
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=supplier)
        if profile_form.is_valid():
            sup = profile_form.save()
            if int(sup.profile_completion_status) < 0:
                sup.profile_completion_status = 0
                sup.save()
            redirect_url = sup.get_profile_completion_status_redirect_url()
            return HttpResponseRedirect(redirect_url)
        else:
            return HttpResponseRedirect("/supplier/profile/info/")
    else:
        
        return render(request, "supplier/supplier_profile.html", 
            {'user': user, 'supplier': supplier, 'salutations': salutations})

def supplier_profile_json(request, id):
    supplier = Supplier.objects.get(id=id)
    data = serializers.serialize('json', [supplier,])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data, content_type='application/json')


@login_required
def comapny_info(request):
    '''
    # Geting user and supplier logged in
    # Check if this supplier already complated the supplier info status = 0
    # Getting or creating SupplierCompany
    # 
    '''
    import pdb; pdb.set_trace();
    user = request.user
    sup = Supplier.objects.get(user=user)
    ps_categories = ProductAndServiceCategory.objects.all()
    try:
        comp, created = SupplierCompany.objects.get_or_create(supplier=sup)
        if not created:
            capability = comp.capability
            selected_categories = comp.ps_categories.all()

    except Exception, e:
        raise e
    if sup.profile_completion_status >= 0:
        if request.method == 'POST':            
            if not created:
                # If not created user is editing this form and capability for this comp is already set
                
                capability_form = CapabilityForm(request.POST, instance=capability)
                capability = capability_form.save()
            else:
                capability_form = CapabilityForm(request.POST)
                capability = capability_form.save()
                # If created is true means this is the first time user filling this comp info
                # So profile_completion_status is set to 1
            sup.profile_completion_status = 1
            sup.save()

            comp_form = CompInfoForm(request.POST, instance=comp)
            if comp_form.is_valid():
                try:
                    comp = comp_form.save()
                    comp.capability = capability
                    comp.save()    
                except Exception, e:
                    raise e
                redirect_url = sup.get_profile_completion_status_redirect_url()
                return HttpResponseRedirect(redirect_url)
                
        else:
            comp_form = CompInfoForm()
            capability_form = CapabilityForm()

            return render(request, "supplier/comapny_info.html", 
                {'capability_form': capability_form, 'user': user, 'supplier': sup, 
                'ps_categories': ps_categories, 'selected_categories': selected_categories})
    else:
        messages.warning(request, 'You must fill supplier info before supplier company info')
        return HttpResponseRedirect("/supplier/profile/info/")

    

@login_required
def comapny_info_json(request, supplier_id):
    from supplier.serializer import *
    supplier = Supplier.objects.get(id=supplier_id)
    supplier_company = SupplierCompany.objects.get(supplier=supplier)
    serializer = CompanySerializer(supplier_company)
    data = json.dumps(serializer.data)
    return HttpResponse(data, content_type='application/json')


def company_revenue(request):
    
    user = request.user
    supplier = Supplier.objects.get(user=user)
    company = SupplierCompany.objects.get(supplier=supplier)
    if request.method == 'POST':
        # import pdb; pdb.set_trace()
        revenue, created = CompanyRevenue.objects.get_or_create(company=company)
        revenue_form = RevenueForm(request.POST, instance=revenue)
        
        if created:
            address_form = AddressForm(request.POST)
        else:
            pay_address = revenue.payment_address
            address_form = AddressForm(request.POST, instance=pay_address)

        if revenue_form.is_valid() and address_form.is_valid():
            comp_rev = revenue_form.save()
            pay_address = address_form.save()
            if created:
                comp_rev.payment_address = pay_address
                comp_rev.save()
            if supplier.profile_completion_status == '1':
                supplier.profile_completion_status = 2
                supplier.save()
            
            redirect_url = supplier.get_profile_completion_status_redirect_url()
            return HttpResponseRedirect(redirect_url)
    else:
        revenue_form = RevenueForm()


        return render(request, "supplier/company_revenue.html", 
        {'sales': ANNUAL_SALE, 'revenue_form': revenue_form})

@login_required
def company_revenue_json(request, supplier_id):
    from supplier.serializer import *
    supplier = Supplier.objects.get(id=supplier_id)
    supplier_company = SupplierCompany.objects.get(supplier=supplier)
    comp_revenue = CompanyRevenue(company=supplier_company)
    serializer = RevenueSerializer(comp_revenue)
    data = json.dumps(serializer.data)
    return HttpResponse(data, content_type='application/json')



def company_contacts(request):

    return render(request, "supplier/company_contacts.html", {})


def company_licenses(request):
    """
    Controller for company license based on user's request
    :param request:
    :return: HTTPResponse
    """
    user = request.user
    supplier = Supplier.objects.get(user=user)
    company = SupplierCompany.objects.get(supplier=supplier)
    if request.method == 'POST':
        company_license_instance, created = CompanyLicense.objects.get_or_create(company=company)
        license_form = CompanyLicenseForm(request.POST, instance=company_license_instance)
        if license_form.is_valid():
            comp_license = license_form.save()
    else:
        license_form = CompanyLicenseForm()
    return render(request, "supplier/company_licenses.html", {'supplier' : supplier,
                                                              'license_form' : license_form,
                                                             'company' : company })

@login_required
def company_licenses_json(request, supplier_id):
    """
    API for company license Model based on supplier ID
    :param request:
    :param supplier_id:
    :return:HttpResponse as JSON
    """
    from supplier.serializer import *
    supplier = Supplier.objects.get(id=supplier_id)
    supplier_company = SupplierCompany.objects.get(supplier=supplier)
    comp_license = CompanyLicense.objects.get(company=supplier_company)
    serializer = CompanyLicenseSerializer(comp_license)
    data = json.dumps(serializer.data)
    return HttpResponse(data, content_type='application/json')




def company_products_services(request):
    """
    Controller for company product and service based on user's request
    :param request:
    :return: HTTPResponse
    """
    user = request.user
    supplier = Supplier.objects.get(user=user)
    company = SupplierCompany.objects.get(supplier=supplier)
    if request.method == 'POST':
        company_product_service_instance, created = CompanyProductService.objects.get_or_create(company=company)
        product_service_form = CompanyProductServiceForm(request.POST, instance=company_product_service_instance)
        if product_service_form.is_valid():
            company_product_service = product_service_form.save()
    else:
        license_form = CompanyLicenseForm()

    return render(request, "supplier/company_products_services.html", {'supplier' : supplier, 'company' : company})

@login_required
def company_products_services_json(request, supplier_id):
    """
    API for company product service Model based on supplier ID
    :param request:
    :param supplier_id:
    :return:HttpResponse as JSON
    """
    from supplier.serializer import *
    supplier = Supplier.objects.get(id=supplier_id)
    supplier_company = SupplierCompany.objects.get(supplier=supplier)
    comp_product_service = CompanyProductService.objects.get(company=supplier_company)
    serializer = CompanyProductServiceSerializer(comp_product_service)
    data = json.dumps(serializer.data)
    return HttpResponse(data, content_type='application/json')




def company_certification(request):
    cert_names = CertificateName.objects.all()
    user = request.user
    supplier = Supplier.objects.get(user=user)
    sup_comp, created = SupplierCompany.objects.get_or_create(supplier=supplier)
    if request.method == 'POST':
        certificate_name_list = request.POST.getlist('certificate_name')
        for i in range(0, len(certificate_name_list)):
            cert_name = CertificateName.objects.get(id=certificate_name_list[i])
            comp_cert, created = CompanyCertification.objects.get_or_create(certificate_name=cert_name, company=sup_comp)
            comp_cert.cert_number = request.POST.getlist('cert_number')[i]
            comp_cert.category = request.POST.getlist('category')[i]
            cert_date = request.POST.getlist('certification_date')[i]
            comp_cert.certification_date = datetime.datetime.strptime(cert_date, '%m/%d/%Y')

            expire_date = request.POST.getlist('expire_date')[i]
            comp_cert.expire_date = datetime.datetime.strptime(expire_date, '%m/%d/%Y')

            comp_cert.certificate_duration = request.POST.getlist('certificate_duration')[i]
            # comp_cert.upload_certificate = request.FILES.getlist('upload_certificate')[i]
            comp_cert.save()
        supplier.profile_completion_status = 6
        supplier.save()

        redirect_url = supplier.get_profile_completion_status_redirect_url()
        return HttpResponseRedirect(redirect_url)
    else:
        pass

    return render(request, "supplier/company_certification.html", {'cert_names': cert_names})

def supplier_submission_status(request):
    user = request.user
    supplier = Supplier.objects.get(user=user)
    selected_buyers = SupplierSelectedBuyers.objects.filter(supplier=supplier)

    return render(request, "supplier/supplier-submission.html", 
        {'buyers': selected_buyers})


@login_required
def company_certification_json(request, supplier_id):
    """
    API for company certification Model based on supplier ID
    :param request:
    :param supplier_id:
    :return:HttpResponse as JSON
    """
    from supplier.serializer import *
    supplier = Supplier.objects.get(id=supplier_id)
    supplier_company = SupplierCompany.objects.get(supplier=supplier)
    comp_product_service = CompanyCertification.objects.get(company=supplier_company)
    serializer = CompanyCertificationSerializer(comp_product_service)
    data = json.dumps(serializer.data)
    return HttpResponse(data, content_type='application/json')

