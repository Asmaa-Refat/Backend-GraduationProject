from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import BranchSerializer, AgencySerializer
from FacilityApp.models import Service
from rest_framework.parsers import JSONParser
from AgencyApp.models import Branch, Agency
from django.core import serializers


@csrf_exempt   
def GetBranchesForAgencyApi(request):
    if request.method == 'POST':
        agencyData = JSONParser().parse(request)
        agencyObj = Agency.objects.get(name = agencyData['agencyName'])   
        branches = agencyObj.branches.all()
        response = []
        for branch in branches:
            response.append(branch.name)
        return JsonResponse (response, safe=False)
    else:
        return JsonResponse("Error: Wrong Method Type", status=400)

@csrf_exempt 
def GetAgenciesApi(request):
    if request.method == 'GET':
        agencies = Agency.objects.all()  
        response = []
        for agency in agencies:
            response.append(agency.name)
        return JsonResponse (response, safe=False)
    else:
        return JsonResponse("Error: Wrong Method Type", status=400)

@csrf_exempt 
def GetAgenciesForAdminApi(request):
    if request.method == 'POST':
        agencies = Agency.objects.all()
        response = []
        for agency in agencies:
            agencyData = AgencySerializer(agency)
            agencyData2 = agencyData.data
            branchNames = set()
            serviceNames = set()
            for branch in agencyData2['branches']:
                branchName = branch['name']
                branchNames.add(branchName)
                for service in branch['services']:
                    serviceNames.add(service['name'])
            newAgencyData = {
                "agencyName": agencyData2['name'],
                "branches": list(branchNames),
                "services": list(serviceNames)
            }
            response.append(newAgencyData)
    return JsonResponse(response, safe=False)




