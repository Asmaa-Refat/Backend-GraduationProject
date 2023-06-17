from django.views.decorators.csrf import csrf_exempt
from FacilityApp.models import Facility
from AgencyApp.models import Branch
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from ModelApp.models import Review
from AuthApp.models import Citizen, AgencySupervisor, BranchSupervisor
from ModelApp.MachineModel.sentimentanalysis_gpmodel import prediction
from AuthApp.serializers import CitizenSignupSerializer, BranchSupervisorSignupSerializer, AgencySupervisorSignupSerializer
from ModelApp.serializers import ReviewSerializer
from django.core.files.storage import default_storage
from rest_framework.response import Response

@csrf_exempt
def CitizenSignupApi(request):
    if request.method == 'POST':
        citizen_data=JSONParser().parse(request)
        citizen_serializer = CitizenSignupSerializer(data=citizen_data)
        if citizen_serializer.is_valid():
            citizen_serializer.save()
            return JsonResponse("Added Successfully!!", safe=False)
        return JsonResponse("Failed to Add.", safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)

@csrf_exempt
def CitizenLoginApi(request):
    if request.method=='POST':
        citizen_data=JSONParser().parse(request)
        if Citizen.objects.filter(email=citizen_data['email'] , password=citizen_data['password']):
            return JsonResponse("LoggedIn Successfully!!" , safe=False)
        return JsonResponse("Invalid email or password.",safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)

@csrf_exempt
def CitizenEditProfileApi(request):
    if request.method=='POST':
        citizen_data=JSONParser().parse(request)
        CurrentCitizen = Citizen.objects.get(nationalId=citizen_data['nationalId'])
        CurrentCitizen.name = citizen_data['name']
        CurrentCitizen.email = citizen_data['email']
        CurrentCitizen.password = citizen_data['password']
        CurrentCitizen.phoneNumber = citizen_data['phoneNumber']
        CurrentCitizen.save()
        return JsonResponse("Data updated Successfully!!" , safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)


@csrf_exempt
def CitizenAddReviewApi(request):
    if request.method == 'POST':
        review_data=JSONParser().parse(request)
        citizen = Citizen.objects.get(nationalId=review_data['source'])
        facility = Facility.objects.get(name=review_data['destination'])

        newReview = Review()

        newReview.source = citizen
        newReview.destination = facility
        newReview.description = review_data['description']
        newReview.state = review_data['state']
        newReview.polarity = prediction(review_data['description'])[0]

        newReview.save()
        return JsonResponse("Added Successfully!!", safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)


@csrf_exempt
def CitizenReviewsHistoryApi(request):
    if request.method == 'GET':
        citizen_data=JSONParser().parse(request)
        currentCitizen = Citizen.objects.get(nationalId=citizen_data['nationalId'])
        return JsonResponse (str(Review.objects.filter(source = currentCitizen).values()), safe=False)
    else:
       return JsonResponse ("Error: Wrong Method Type",safe=False)   


# GovSupervisor Register and Login
@csrf_exempt
def BranchSupervisorSignupApi(request):
    branchSupervisor_data = JSONParser().parse(request)
    branchSupervisor_serializer = BranchSupervisorSignupSerializer(data = branchSupervisor_data)
    if branchSupervisor_serializer.is_valid():
        branchSupervisor_serializer.save()
        return JsonResponse("Added Successfully!!" , safe=False)
    return JsonResponse("Failed to Add.",safe=False)

@csrf_exempt
def BranchSupervisorLoginApi(request):
    if request.method == 'POST':
        branchSupervisor_data = JSONParser().parse(request)
        if BranchSupervisor.objects.filter(govId = branchSupervisor_data['govId'] , password=branchSupervisor_data['password']):
            return JsonResponse("LoggedIn Successfully!!" , safe=False)
        return JsonResponse("Invalid Id or password.",safe=False)
    

@csrf_exempt
def AgencySupervisorSignupApi(request):
    agencySupervisor_data = JSONParser().parse(request)
    agencySupervisor_serializer = AgencySupervisorSignupSerializer(data = agencySupervisor_data)
    if agencySupervisor_serializer.is_valid():
        agencySupervisor_serializer.save()
        return JsonResponse("Added Successfully!!" , safe=False)
    return JsonResponse("Failed to Add.",safe=False)

@csrf_exempt
def AgencySupervisorLoginApi(request):
    if request.method == 'POST':
        agencySupervisor_data = JSONParser().parse(request)
        if AgencySupervisor.objects.filter(govId = agencySupervisor_data['govId'] , password=agencySupervisor_data['password']):
            return JsonResponse("LoggedIn Successfully!!" , safe=False)
        return JsonResponse("Invalid email or password.",safe=False)

# reviews count based on specific type    
@csrf_exempt
def ServiceReviewsCountApi(request):
    if request.method == 'GET':
        request_data = JSONParser().parse(request)
        facilityObj = Facility.objects.get(name = request_data['serviceName'])
        branchObj = Branch.objects.get(name = request_data['branchName'])

        positiveCount = 0
        negativeCount = 0
        neutralCount = 0

        reviews = Review.objects.filter(destination = facilityObj, relatedBranch = branchObj)
        for review in reviews:
            if review.polarity == "positive":
                positiveCount += 1
            elif review.polarity == "negative":
                negativeCount += 1
            elif review.polarity == "neutral":
                neutralCount += 1

        response_data = {
            'positiveCount': positiveCount,
            'negativeCount': negativeCount,
            'neutralCount': neutralCount
        }

        return JsonResponse(response_data)

    return JsonResponse("Invalid.",safe=False)        

@csrf_exempt
def ServiceReviewsApi(request):
    if request.method == 'GET':
        print(request)
        #request_data = JSONParser().parse(request)
        facilityObj = Facility.objects.get(name = request.GET.get('serviceName'))
        branchObj = Branch.objects.get(name = request.GET.get('branchName'))
        
        reviews = Review.objects.filter(destination = facilityObj, relatedBranch = branchObj)

        positiveList = []
        negativeList = []
        neutralList = []

        for review in reviews:
            dict = {
                    "description":review.description,
                    "state": review.state
                }
            if review.polarity == "positive":  
                positiveList.append(dict)
            elif review.polarity == "negative":
                negativeList.append(dict)
            elif review.polarity == "neutral":
                neutralList.append(dict)
         
        response_data = {
            'positiveList': positiveList,
            'negativeList': negativeList,
            'neutralList': neutralList
        }
        
        return JsonResponse(response_data, safe=False)
    
    return JsonResponse("Invalid.",safe=False)  

@csrf_exempt
def BranchReviewsApi(request):
    if request.method == 'GET':
        request_data = JSONParser().parse(request)
        branchObj = Branch.objects.get(name = request_data['branchName'])

        reviews = Review.objects.filter(relatedBranch = branchObj)

        positiveList = []
        negativeList = []
        neutralList = []

        for review in reviews:
            dict = {
                    "description":review.description,
                    "serviceName":review.destination.name,
                    "state": review.state
                }
            if review.polarity == "positive":  
                positiveList.append(dict)
            elif review.polarity == "negative":
                negativeList.append(dict)
            elif review.polarity == "neutral":
                neutralList.append(dict)
         
        response_data = {
            'positiveList': positiveList,
            'negativeList': negativeList,
            'neutralList': neutralList
        }
        
        return JsonResponse(response_data, safe=False)
    
    return JsonResponse("Invalid.",safe=False)     