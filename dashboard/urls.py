from django.urls import path
from . import views
from dashboard.views import GeneratePDF


urlpatterns = [
    path('', views.login, name="login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('vehicle-book', views.vehicle_book, name="vehicle_book"),
    path('vehicle-book-details/<int:id>/', views.vehicle_book_details, name='vehicle_book_details'),
    path('curd-vehicle-form', views.curd_vehicle_form, name="curd_vehicle_form"),   #sub part
    path('create-new-vehicle-record', views.create_new_vehicle_record, name="create_new_vehicle_record"),   #sub part
    path('update-vehicle-record/<int:id>', views.update_vehicle_record, name="update_vehicle_record"),   #sub part
    path('company-book', views.company_book, name="company_book"),
    path('curd-company-form', views.curd_company_form, name="curd_company_form"),
    path('create-new-company-record', views.create_new_company_record, name="create_new_company_record"),   #sub part
    path('update-company-record/<int:id>', views.update_company_record, name="update_company_record"),   #sub part
    path('logout', views.logout, name="logout"),
    #ledger url
    path('ledger-list', views.ledger_list, name="ledger_list"),
    path('ledger/<uuid:uuid>/update/', views.update_ledger_record, name='update_ledger_record'),
    path('add-new-vehicle-ledger', views.add_new_vehicle_ledger, name="add_new_vehicle_ledger"),
    path('create-new-ledger', views.create_new_ledger, name="create_new_ledger"),
    path('ledger-details/<uuid:uuid>', views.ledger_details, name="ledger_details"),
    path('ledger-details/print-sample/d/<uuid:uuid>', views.ledger_details_print_sample, name="ledger_details_print_sample"),
    path('add-txn-form', views.add_txn_form, name="add_txn_form"),
    path('add-new-txn-details', views.add_new_txn_details, name="add_new_txn_details"),
    #user
    path('user-info', views.user_info, name="user_info"),
    # path('curd-user', views.curd_user, name="curd_user"),  
    # path('create-new-user', views.create_new_user, name="create_new_user"),   #sub part
    # path('update-user/<int:id>', views.update_user, name="update_user"),   #sub part
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('ledger/<uuid:ledger_id>/delete/', views.delete_ledger_record, name='delete_ledger_record'),


    path("genrate-pdf-repot",GeneratePDF.as_view(),name="genrate_pdf_report"),
    path("show-report",views.show_report,name="show_report"),

    
]
