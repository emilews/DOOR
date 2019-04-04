from .models import Registro
from .serializers import DoorCodeSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseNotFound
from passlib.hash import sha256_crypt
from django.db import transaction



#View used as a method to get the code of the user that's asking for it
#It's csrf exempted because we are not connecting from a web app, but an
#android and iOS app
#It only accepts POST http method
#It looks for the email in the DB and returns the code if the email exists
#It returns a 404 code if the email is not in the DB
@csrf_exempt 
def GetCode(request):
    if request.method == 'GET':
        return HttpResponseNotFound("Don't use GET to get codes.")
    if request.method == 'POST':
        data = request.POST
        users = Registro.objects.filter(email=data['email'])
        device = data['device']
        if len(users) == 1 and users[0].device == device:
            return JsonResponse({'code':users[0].password})
        else:
            return HttpResponseNotFound("User not found.")
    return

@csrf_exempt 
@transaction.atomic
def LogIn(request):
    if request.method == 'GET':
        return HttpResponseNotFound("Don't use GET to log in.")
    if request.method == 'POST':
        data = request.POST
        users = Registro.objects.filter(email=data['email'])
        if len(users) == 1:
            if  sha256_crypt.verify(data['password'], users[0].pswd):
                Registro.objects.select_for_update().filter(email=data['email']).update(device=data['device'])
                return JsonResponse({'Status': 'Succesfully logged in!'})
            else:
                return HttpResponseNotFound("Wrong password.")
        else:
            return HttpResponseNotFound("User not found.")           


@csrf_exempt 
def SignUp(request):
    if request.method == 'POST':
        data = request.POST
        users = Registro.objects.filter(email=data['email'])
        if users:
            return HttpResponseNotFound("Email already in use.")
        newcode = 1234
        hash = sha256_crypt.using(rounds=5000).hash(data['password'])
        newuser = Registro.objects.create(nombre=data['name'], email=data['email'], password=newcode, pswd=hash)
        return JsonResponse({'Status': 'Succesfully registered!'})

        
@csrf_exempt
@transaction.atomic
def SetPassword(request):
    if request.method == 'POST':
        data = request.POST
        hash = sha256_crypt.using(rounds=5000).hash(data['password'])
        if Registro.objects.filter(email=data['email']):
            Registro.objects.select_for_update().filter(email=data['email']).update(pswd = hash)
    return JsonResponse({'Success':'200'})