from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from reportlab.pdfgen import canvas
from reportlab.platypus import Table,SimpleDocTemplate,  TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

from django.template.loader import get_template
from django.urls import reverse
from django.views import View

from django.views.generic import TemplateView
from xhtml2pdf import pisa
import os

from users.customcode import authenticate
from django.contrib.auth import login as auth_login
from users.models import CustomUserModel as User
from django.contrib.auth.decorators import login_required
from .models import VehicleRegistration, CompanyRegistration, vehicleLedgerLog, PaymentLog
from core import choice
from django.db.models import Sum
from .utils import render_to_pdf
import datetime

# Create your views here.
def login(request):
    data={}
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        email = request.POST.get("uname",None)
        password = request.POST.get("psw",None)
        if email and password:
            user_obj = User.objects.filter(username=email).first()
            if user_obj:
                check_login = authenticate(username=email, password=password)
                if check_login is not None:
                    auth_login(request, check_login)
                    return redirect('dashboard')
                else:
                    data['error'] = "Incorrect login email and password."
            else:
                data['error'] = "Something wents worng..."
        return redirect("login")
    else:
        return render(request,"login.html",data)
        # return redirect("login")
    # return HttpResponse("MANAGEMENT LOGIN...")


@login_required(login_url='/')
def dashboard(request):
    vechRegObj = VehicleRegistration.objects.order_by('-create_at')[:2]
    ctx = {'vechRegObj': vechRegObj}
    count = VehicleRegistration.objects.count()      
    ctx['count'] = count
    company_count=CompanyRegistration.objects.count()
    ctx['company_count'] = company_count
    ledger_count=vehicleLedgerLog.objects.count()
    ctx['ledger_count'] = ledger_count
    return render(request, 'dashboard.html', ctx)
@login_required(login_url='/')
def vehicle_book(request):
    print("request__________________________________",request)
    ctx = {}
    from_date=request.GET.get("from_date",None)
    to_date = request.GET.get("to_date",None)
    search = request.GET.get("search",None)

    print(from_date)
    print(to_date)
    print(search)
    
    if request.method == "GET":
        vechRegObj = VehicleRegistration.objects.filter(active=1)
        if from_date and to_date:
            print("Date FROM END")
            vechRegObj = vechRegObj.filter(create_at__range=[from_date, to_date])
        # if search:
        #     print("Search Driver")
        #     vechRegObj = vechRegObj.filter(driver_name__icontains=search)
        if search:
            print("Search vehicle_number__icontains")
            vechRegObj = vechRegObj.filter(vehicle_number__icontains=search)
        
        # elif search:
        #     results = VehicleRegistration.objects.filter(
        #     vehicle_number__icontains=search,
        #     driver_name__icontains=search,
        #     active=True
        # ).distinct('id')
        #     ctx['vechRegObj'] = results 
            # ctx['vechRegObj'] = vechRegObj
        # else:  
        #     print("ELSE")
            
        ctx['vechRegObj'] = vechRegObj
        ctx['search'] = search
    return render(request, "vehicle_list.html", ctx)

@login_required(login_url='/')
def vehicle_book_details(request,id):
    ctx = {}
    if request.method == "GET":
    # Fetch the VehicleRegistration object with the specified id
        # id = request.GET.get('id')
        try:
            vechRegObj = VehicleRegistration.objects.get(id=id)
            ctx['vechRegObj'] = vechRegObj
        except VehicleRegistration.DoesNotExist:
            # Handle the case where no VehicleRegistration object is found with the specified id
            pass
    return redirect("vehicle_book")


@login_required(login_url='/')
def company_book(request):
    ctx={}
    from_date=request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    if request.method == "GET":
        if from_date and to_date:
            vechRegObj = CompanyRegistration.objects.filter(create_at__range=[from_date, to_date])
            ctx['vechRegObj'] = vechRegObj  
        else:
            compRegObj = CompanyRegistration.objects.filter(active=1)
            ctx['compRegObj']=compRegObj
    return render(request,"company_list.html",ctx)

@login_required(login_url='/')
def curd_company_form(request):
    ctx={}
    company_id = request.GET.get("company_id",None)
    if company_id:
        companyRegUpdateObj = CompanyRegistration.objects.filter(id=company_id).last()
        ctx['companyRegUpdateObj']=companyRegUpdateObj
        return render(request,"sub/company_curd_form.html",ctx)
    return render(request,"",ctx)

@login_required(login_url='/')
def curd_vehicle_form(request):
    ctx={}
    vehicle_id = request.GET.get("vehicle_id",None)
    if vehicle_id:
        vechRegUpdateObj = VehicleRegistration.objects.filter(id=vehicle_id).last()
        ctx['vechRegUpdateObj']=vechRegUpdateObj
        return render(request,"sub/vech_curd_form.html",ctx)
    return render(request,"",ctx)

@login_required(login_url='/')
def create_new_vehicle_record(request):
    ctx={}
    if request.method == "POST":
        vehicle_number = request.POST.get("vehicle_number",None)
        driver_name = request.POST.get("driver_name",None)
        driver_mobile = request.POST.get("driver_mobile",None)
        if vehicle_number and driver_mobile and driver_name:
            x = VehicleRegistration(
                vehicle_number = vehicle_number, 
                driver_name = driver_name,
                driver_mobile = driver_mobile,
                user = request.user
            )
            x.save()
    return redirect("vehicle_book")

@login_required(login_url='/')
def update_vehicle_record(request,id):
    ctx={}
    if request.method == "POST":
        vehicle_number = request.POST.get("vehicle_number",None)
        driver_name = request.POST.get("driver_name",None)
        driver_mobile = request.POST.get("driver_mobile",None)

        VehicleRegistration.objects.filter(id=id).update(
            vehicle_number = vehicle_number, 
            driver_name = driver_name,
            driver_mobile = driver_mobile,
        )
    return redirect("vehicle_book")

@login_required(login_url='/')
def create_new_company_record(request):
    ctx={}
    if request.method == "POST":
        company_name = request.POST.get("company_name",None)
        company_address = request.POST.get("company_address",None)
        if  company_name and company_address:
            x = CompanyRegistration(
                company_name = company_name,
                company_address = company_address,
                user = request.user
            )
            x.save()
    return redirect("company_book")

@login_required(login_url='/')
def update_company_record(request,id):
    ctx={}
    if request.method == "POST":
        company_name = request.POST.get("company_name",None)
        company_address = request.POST.get("company_address",None)

        CompanyRegistration.objects.filter(id=id).update(
            company_name = company_name,
            company_address = company_address,
        )
    return redirect("company_book")

@login_required(login_url='/')
def logout(request):
    from django.contrib import auth
    auth.logout(request)
    return redirect('/')

#ledger_list
@login_required(login_url='/')
def ledger_list(request):
    ctx={}
    ctx['vichle_obj']=VehicleRegistration.objects.filter(active=True)
    ctx['company_obj']=CompanyRegistration.objects.filter(active=True)

    vehicle_id = request.GET.get("vehicle",None)
    company_id = request.GET.get("company",None)
    if vehicle_id:
        ctx['vehicle'] = int(vehicle_id)
    if company_id:
        ctx['company'] = int(company_id)


    # search = request.GET.get("search",None)
    from_date = request.GET.get("from_date",None)
    to_date = request.GET.get("to_date",None)
    if from_date:
        ctx['from_date']=from_date
    if to_date:
        ctx['to_date']=to_date
    if request.method == "GET":
        # if search:
        #     print("Search vehicle_number__icontains")
        #     ledgerObj = VehicleRegistration.objects.filter(vehicle_number__icontains=search)
        #     ids = ledgerObj.values_list('id', flat=True) # Retrieve ids of matching objects   
        #     ctx['ids'] = ids     
        # else:

        if from_date and to_date:
            ledgerObj = vehicleLedgerLog.objects.filter(date__gte=from_date, date__lte=to_date).order_by("-id")
        else:
            ledgerObj = vehicleLedgerLog.objects.all().order_by("-id")
        
        if vehicle_id:
            ledgerObj = ledgerObj.filter(vehicle__id = int(vehicle_id))
        
        if company_id:
            ledgerObj = ledgerObj.filter(company__id = int(company_id))
    
        ctx['ledgerObj']=ledgerObj
        # ctx['search'] = search
    return render(request,"ledger_list.html",ctx)


@login_required(login_url='/')
def add_new_vehicle_ledger(request):
    ctx={}
    vechRegObj = VehicleRegistration.objects.filter(active=1)
    ctx['vechRegObj']=vechRegObj

    company_obj = CompanyRegistration.objects.filter(active=1)
    ctx['company_obj'] = company_obj
    
    return render(request,"sub/add_ledger_form.html",ctx)

@login_required(login_url='/')
def create_new_ledger(request):
    ctx={}
    if request.method == "POST":
        fdate = request.POST.get("fdate",None) 
        vehicle = request.POST.get("vehicle",None) 
        company = request.POST.get("company",None) 
        # amount = request.POST.get("amount",None) 

        if fdate and vehicle and company:
            x = vehicleLedgerLog(
                date = fdate,
                vehicle_id = vehicle,
                company_id = company, 
                # total_amount = amount,
                user = request.user,
            )
            x.save()
    # return render(request,"ledger_record_details.html",ctx)
    return redirect('ledger-details/'+str(x.uuid))

def update_ledger_record(request, uuid):
    print(uuid)
    if request.method == 'POST':
        vehicle_obj = vehicleLedgerLog.objects.filter(uuid=uuid).last()
        if vehicle_obj:
            ufdate = request.POST.get("ufdate",None) 
            uvehicle = request.POST.get("uvehicle",None) 
            ucompany = request.POST.get("ucompany",None) 
            uamount = request.POST.get("uamoount",None)
            vehicleLedgerLog.objects.filter(uuid=uuid).update(
                date = ufdate,
                vehicle_id = uvehicle,
                company_id = ucompany, 
                # total_amount = uamount,
            )
            
    return redirect('/ledger-details/'+str(uuid))
def delete_ledger_record(request, ledger_id):
    ledger = get_object_or_404(vehicleLedgerLog, uuid=ledger_id)
    ledger.delete()
    return redirect('ledger_list')


@login_required(login_url='/')
def ledger_details(request,uuid):
    ctx={}
    print(uuid)
    vehicle_obj = vehicleLedgerLog.objects.filter(uuid=uuid).last()
    ctx['vehicle_obj']=vehicle_obj

    paymentLogObj = PaymentLog.objects.filter(ledger_log__uuid=uuid).order_by("-id")
    ctx['paymentLogObj']=paymentLogObj

    # total_amount = vehicle_obj.total_amount
    total_txn_amount_crt = PaymentLog.objects.filter(ledger_log__uuid=uuid).aggregate(sum=Sum('crt_amount'))['sum']
    if total_txn_amount_crt==None:
        total_txn_amount_crt=0

    total_txn_amount_dbt = PaymentLog.objects.filter(ledger_log__uuid=uuid).aggregate(sum=Sum('dbt_amount'))['sum']
    if total_txn_amount_dbt==None:
        total_txn_amount_dbt=0
    
    # balance = total_amount-total_txn_amount
    ctx['total_txn_amount']=total_txn_amount_crt
    ctx['total_txn_amount_dbt']=total_txn_amount_dbt
    ctx['balance']=vehicle_obj.balance

    vechRegObj = VehicleRegistration.objects.filter(active=1)
    ctx['vechRegObj']=vechRegObj

    company_obj = CompanyRegistration.objects.filter(active=1)
    ctx['company_obj'] = company_obj
    return render(request,"ledger_record_details.html",ctx)

@login_required(login_url='/')
def ledger_details_print_sample(request,uuid):
    ctx={}
    print(uuid)
    vehicle_obj = vehicleLedgerLog.objects.filter(uuid=uuid).last()
    ctx['vehicle_obj']=vehicle_obj

    paymentLogObj = PaymentLog.objects.filter(ledger_log__uuid=uuid).order_by("id")
    ctx['paymentLogObj']=paymentLogObj

    if paymentLogObj:
        ctx['sd'] = paymentLogObj.first().date
        ctx['ed'] = paymentLogObj.last().date

    total_txn_amount_crt = PaymentLog.objects.filter(ledger_log__uuid=uuid).aggregate(sum=Sum('crt_amount'))['sum']
    if total_txn_amount_crt==None:
        total_txn_amount_crt=0

    total_txn_amount_dbt = PaymentLog.objects.filter(ledger_log__uuid=uuid).aggregate(sum=Sum('dbt_amount'))['sum']
    if total_txn_amount_dbt==None:
        total_txn_amount_dbt=0
    
    ctx['total_txn_amount']=total_txn_amount_crt
    ctx['total_txn_amount_dbt']=total_txn_amount_dbt
    ctx['balance']=vehicle_obj.balance

    vechRegObj = VehicleRegistration.objects.filter(active=1)
    ctx['vechRegObj']=vechRegObj

    company_obj = CompanyRegistration.objects.filter(active=1)
    ctx['company_obj'] = company_obj
    return render(request,"pdf_report/view_details_sheet_report.html",ctx)


@login_required(login_url='/')
def add_txn_form(request):
    ctx={}
    payment_mode_choice = choice.PaymentMode.CHOICES
    ctx['payment_mode_choice']=payment_mode_choice
    return render(request,"sub/add_transcation_form.html",ctx)

@login_required(login_url='/')
def add_new_txn_details(request):
    ctx={}
    date = request.GET.get("date",None)
    txn_mode = request.GET.get("txn_mode",None)
    amount = request.GET.get("amount",None)
    remark = request.GET.get("remark",None)
    uuid = request.GET.get("uuid",None)
    txn_type = request.GET.get("txn_type",None)

    print(date)
    print(txn_mode)
    print("AMOUNT: ",amount)
    print(remark)
    print(uuid)
    print(txn_type)
    print(type(txn_type))
    
    if date and txn_mode and amount and remark and uuid and txn_type:
        x = PaymentLog(
            ledger_log = vehicleLedgerLog.objects.filter(uuid=uuid).last(),
            date = date,
            mode = txn_mode,
            remark = remark,
            user = request.user,
        )
        # x.save()

        if txn_type == "1":   #Credit
            print("CRDIT VIEW TXN")
            x.type = 1
            x.crt_amount = int(amount)
            x.save()
        elif txn_type == "2":     #Debit
            print("DEBIT VIEW TXN")
            x.type = 2
            x.dbt_amount = int(amount)
            x.save()
        else:
            print("Else")
            # x.delete()

    
    return JsonResponse({},status=200)


#user
# @login_required(login_url='/')
# def curd_user(request):
#     ctx={}
#     user_id = request.GET.get("user_id",None)
#     if user_id:
#         userObj = User.objects.filter(id=user_id).last()
#         ctx['userObj']=userObj
#         return render(request,"sub/user_curd.html",ctx)
#     return render(request,"",ctx)

@login_required(login_url='/')
def user_info(request):
    ctx={}
    if request.method == "GET":
        userObj = User.objects.filter(is_active=True)
        ctx['userObj']=userObj
    return render(request,"user.html",ctx)

# @login_required(login_url='/')
# def update_user(request,id):
#     ctx={}
#     if request.method == "POST":
#         first_name = request.POST.get("first_name",None)
#         last_name = request.POST.get("last_name",None)
#         username = request.POST.get("username",None)
#         email = request.POST.get("email",None)
#         mobile = request.POST.get("mobile",None)

#         User.objects.filter(id=id).update(
#             first_name = first_name, 
#             last_name = last_name,
#             username = username,
#             email = email,
#             mobile = mobile,
#         )
#     return redirect("user_info")

# @login_required(login_url='/')
# def create_new_user(request):
#     ctx={}
#     if request.method == "POST":
#         first_name = request.POST.get("first_name",None)
#         last_name = request.POST.get("last_name",None)
#         username = request.POST.get("username",None)
#         email = request.POST.get("email",None)
#         mobile = request.POST.get("mobile",None)
#         if  first_name and last_name:
#             x = User(
#                 first_name = first_name, 
#                 last_name = last_name,
#                 username = username,
#                 email = email,
#                 mobile = mobile
#             )
#             x.save()
#     return redirect("user_info")

# def search(request):
#     if request.method == 'POST':
#         search_query = request.POST.get('search_query')
#         vehicles = VehicleRegistration.objects.filter(Q(vehicle_number__icontains=search_query) | Q(driver_name__icontains=search_query))
#         data = {'vehicles': list(vehicles.values())}
#         return JsonResponse(data)

#     return render(request, 'search.html')

def generate_pdf(request):
    # Create a new PDF object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # Query data from the database
    vecObj = vehicleLedgerLog.objects.all()
    pdf = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
     # Create a table from the data
    table_data = []
    headers = ['Date','Vehicle Number', 'Driver Name', 'Company Name','Total Amount','Received Amount', 'Pending Amount']
    table_data.append(headers)

    for row in vecObj:
        row_data = [row.date,row.vehicle.vehicle_number, row.vehicle.driver_name, row.company.company_name,row.total_amount,row.recived_amount,0]
        table_data.append(row_data)

    table = Table(table_data)

     # Apply table styles
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),

        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),

        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        ('TEXTCOLOR',(0,1),(-1,-1),colors.black),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 10),

        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    # Close the PDF
    pdf.build([table])

    return response


def show_report(request):
    ctx={}
    from_date = request.GET.get("from_date",None)
    to_date = request.GET.get("to_date",None)
    vehicle = request.GET.get("vehicle",None)
    company = request.GET.get("company",None)

    if vehicle:
        ledgerObj = vehicleLedgerLog.objects.filter(vehicle__id=int(vehicle))

        if from_date and to_date:
            ledgerObj = ledgerObj.filter(date__gte=from_date, date__lte=to_date)
        
        if company:
            ledgerObj = ledgerObj.filter(company__id = int(company))
        
        print("*"*200)
        print(ledgerObj)

        total_amount = ledgerObj.aggregate(sum=Sum('total_amount'))['sum']
        print(total_amount) 

        ledger_ids_list = list(ledgerObj.values_list('id',flat=True))
        print(ledger_ids_list)

        recived_amount = PaymentLog.objects.filter(ledger_log__id__in=ledger_ids_list).aggregate(sum=Sum('amount'))['sum']
        print(recived_amount)
        ledgerObj = ledgerObj.order_by("date")
        log_list = []
        for i in ledgerObj:
            temp_dict={}
            temp_dict['date'] = i.date
            temp_dict['vehicle'] = i.vehicle.vehicle_number
            temp_dict['driver'] = i.vehicle.driver_name
            temp_dict['company'] = i.company.company_name
            payment_log = PaymentLog.objects.filter(ledger_log__id=i.id).last()
            if payment_log:
                temp_dict['company_remark'] = f"{i.company.company_name} / {payment_log.remark}"
            else:
                temp_dict['company_remark'] = ''
            temp_dict['total_amount'] = i.total_amount
            recAmount = PaymentLog.objects.filter(ledger_log__id=i.id).aggregate(sum=Sum('amount'))['sum']
            if recAmount==None:
                recAmount=0
            temp_dict['rec_amount']=recAmount
            temp_dict['balance']=i.total_amount-recAmount
            log_list.append(temp_dict)
        
        print(log_list)

        
        ctx['sd'] = ledgerObj.first().date
        ctx['ed'] = ledgerObj.last().date

        ctx['ledgerObj']=ledgerObj
        ctx['total_amount']=total_amount
        ctx['vehicle']=ledgerObj.last().vehicle.vehicle_number
        if company:
            ctx['company']=company
        ctx['vehicle']=ledgerObj.last().vehicle.vehicle_number
        if recived_amount:
            ctx['recived_amount']=recived_amount
            ctx['balance']=total_amount - recived_amount
        else:
            ctx['recived_amount']=0
        
        ctx['log_list']=log_list
    return render(request,"pdf_report/view_sheet_report.html",ctx)



# def generate_pdf_report(request):
#     # html = template.render({})
#     pdf = render_to_pdf('pdf_report/view_sheet_report.html', {'name':"VehicleLedger"})
#     if pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename=BalanceSheetReport-{date}.pdf'.format(date=datetime.datetime.now().strftime('%d-%m-%Y'),)
#         return response


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('pdf_report/view_sheet_report.html')
        context = {
            'name': 'VehicleLedger',
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="BalanceSheetReport.pdf"'
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
