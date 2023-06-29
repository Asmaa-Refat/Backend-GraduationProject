import json
from django.shortcuts import render
from .models import Administrator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from AuthApp.models import AgencySupervisor, BranchSupervisor
from FacilityApp.models import Document, Service, App
from AgencyApp.models import Agency, Branch


@csrf_exempt
def AdministratorLoginApi(request):
    if request.method == 'POST':
        administrator_data = JSONParser().parse(request)
        obj = Administrator.load()
        if obj.username == administrator_data['username'] and obj.password  == administrator_data['password']:
            return JsonResponse("LoggedIn Successfully!!", safe=False)
        return JsonResponse("Invalid username or password.",safe=False)     

@csrf_exempt
def GetAllUnapprovedAgencySupervisorsApi(request):
    if request.method=='POST':
        agencySupervisorObjects = AgencySupervisor.objects.filter(isApproved = False)
        agencySupervisorsList = []
        for agencySupervisor in agencySupervisorObjects:
            agencySupervisorData = {
                "name": agencySupervisor.name,
                "govId":agencySupervisor.govId
            }
            agencySupervisorsList.append(agencySupervisorData)
        return JsonResponse(agencySupervisorsList,safe=False)

@csrf_exempt
def GetAllUnapprovedBranchSupervisorsApi(request):
    if request.method=='POST':
        branchSupervisorObjects = BranchSupervisor.objects.filter(isApproved = False)
        branchSupervisorsList = []
        for agencySupervisor in branchSupervisorObjects:
            branchSupervisorData = {
                "name": agencySupervisor.name,
                "govId":agencySupervisor.govId
            }
            branchSupervisorsList.append(branchSupervisorData)
        return JsonResponse(branchSupervisorsList,safe=False)
    
@csrf_exempt
def DeleteAgencySupervisorFromDatabaseApi(request):
    if request.method=='POST':
        request_data = JSONParser().parse(request)
        try:
            agencySupervisor = AgencySupervisor.objects.get(govId = request_data['govId'])
            agencySupervisor.delete()
        except AgencySupervisor.DoesNotExist:
            return JsonResponse("AgencySupervisor Not Found!!",safe=False) 
        return JsonResponse("AgencySupervisor Deleted Successfully!!",safe=False)

@csrf_exempt
def DeleteBranchSupervisorFromDatabaseApi(request):
    if request.method=='POST':
        request_data = JSONParser().parse(request)
        try:
            branchSupervisor = BranchSupervisor.objects.get(govId = request_data['govId'])
            branchSupervisor.delete()
        except BranchSupervisor.DoesNotExist:
            return JsonResponse("BranchSupervisor Not Found!!",safe=False) 
        return JsonResponse("BranchSupervisor Deleted Successfully!!",safe=False)
    
@csrf_exempt
def ApproveAgencySupervisorApi(request):
    if request.method=='POST':
        request_data = JSONParser().parse(request)
        try:
            agencySupervisor = AgencySupervisor.objects.get(govId = request_data['govId'])
            agencySupervisor.isApproved = True
            agencySupervisor.save()
        except AgencySupervisor.DoesNotExist:
            return JsonResponse("AgencySupervisor Not Found!!",safe=False) 
        return JsonResponse("AgencySupervisor Approved Successfully!!",safe=False)

@csrf_exempt
def ApproveBranchSupervisorApi(request):
    if request.method=='POST':
        request_data = JSONParser().parse(request)
        try:
            branchSupervisor = BranchSupervisor.objects.get(govId = request_data['govId'])
            branchSupervisor.isApproved = True
            branchSupervisor.save()
        except BranchSupervisor.DoesNotExist:
            return JsonResponse("BranchSupervisor Not Found!!",safe=False) 
        return JsonResponse("BranchSupervisor Approved Successfully!!",safe=False)
 
@csrf_exempt
def CreateAgencyApi(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        agencyName = data['agencyName']
        branches_data = data['branches']
        new_agency = Agency(name=agencyName)
        new_branches = []
        for branch_data in branches_data:
            branch_services_data = branch_data['services']
            branchName = branch_data['branchName']+' '+agencyName
            new_branch = Branch(name=branchName)
            new_services = []
            for service_data in branch_services_data:
                documents_data = service_data['documents']
                service = Service(name=service_data['serviceName'], type=service_data['serviceType'])
                service_exists = Service.objects.filter(name=service.name, type=service.type).exists()
                if service_exists:
                    print(service_exists)
                    service = Service.objects.get(name=service.name, type=service.type)

                new_documents = []
                for document_data in documents_data:
                    document = Document(name=document_data['documentName'])
                    document_exists = Document.objects.filter(name=document.name).exists()
                    if document_exists:
                        document = Document.objects.get(name=document.name)
                    else:
                        document.save()
                    new_documents.append(document)

                #document_ids = new_documents.values_list('id', flat=True)  # Get a list of document IDs
                service_exists = Service.objects.filter(name=service.name, type=service.type).exists()
                if service_exists:
                    service = Service.objects.get(name=service.name, type=service.type)
                else:
                    #service.documents.set([new_documents[0]])
                    service.save()
                    service.documents.set(new_documents)
                    service.save()
                new_services.append(service)

            branch_exists = Branch.objects.filter(name=branchName).exists()
            if branch_exists:
                new_branch = Branch.objects.get(name=branchName)
            else:
                new_branch.save()
                new_branch.services.set(new_services)
                new_branch.save()
            new_branches.append(new_branch)

        agency_exists = Agency.objects.filter(name=agencyName).exists()
        if agency_exists:
            new_agency = Agency.objects.get(name=agencyName)
        else:
            new_agency.save()
            new_agency.branches.set(new_branches)
            new_agency.save()
        return JsonResponse({'status': 'تم اضافه الجهه بنجاح'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def AddAppApi(request):
    if request.method=='POST':
        app_data = JSONParser().parse(request)
        newAPP = App(
                name = app_data["name"],
                rate = app_data["rate"],
                englishName = app_data["englishName"],
                link = app_data["link"],
                description = app_data["description"],
                cover = app_data["cover"]
        )
        newAPP.save()
        return JsonResponse("Added Successfully!!" , safe=False)
    

@csrf_exempt
def DeleteAppApi(request):
    if request.method=='POST':
        app_data = JSONParser().parse(request)
        try:
            app_obj = App.objects.filter(name = app_data["name"])
            app_obj.delete()
        except App.DoesNotExist:
            return JsonResponse("app Not Found!!",safe=False) 
        return JsonResponse("App Deleted Successfully!!", safe=False)