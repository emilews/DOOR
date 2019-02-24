from .models import Registro
from .serializers import DoorCodeSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseNotFound
from passlib.hash import sha256_crypt
   

@csrf_exempt 
def GetCode(request):
    if request.method == 'POST':
        data_unicode = request.body.decode('utf-8')
        body = json.loads(data_unicode)
        users = Registro.objects.filter(email=body['email'])
        if users:
            return JsonResponse({'code':users[0].password})
        else:
            return HttpResponseNotFound("User not found.")
    return

@csrf_exempt 
def LogIn(request):
    if request.method == 'POST':
        data_unicode = request.body.decode('utf-8')
        body = json.loads(data_unicode)
        email = body['email']
        users = Registro.objects.filter(email=body['email'])
        if users:
            if  sha256_crypt.verify(body['password'], users[0].pswd):
                return JsonResponse({'code':users[0].password})
            else:
                return HttpResponseNotFound("Wrong password.")
        else:
            return HttpResponseNotFound("User not found.")           

@csrf_exempt 
def GetPassword(request):
    if request.method == 'POST':
        data_unicode = request.body.decode('utf-8')
        body = json.loads(data_unicode) 
        email = body['email']
        hash = sha256_crypt.using(rounds=5000).hash(body['password'])
        if Registro.objects.filter(email=body['email']):
            Registro.objects.select_for_update().filter(email=body['email']).update(pswd = hash)
        
    return JsonResponse({'Success':'200'})