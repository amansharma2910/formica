from django.shortcuts import render, redirect
from django.http import JsonResponse
# Create your views here.
from .serializer import FormCreateSerializer, FormResponseSerializer, DiscordUserSerializer
from .models import FormCreate, FormResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response 
import requests
import environ 
from dotenv import load_dotenv
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
load_dotenv()


redirect_url_discord = "https://discord.com/api/oauth2/authorize?client_id=728306573696303135&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Flogin%2Fredirect%2F&response_type=code&scope=identify"

@login_required(login_url='login/')
@api_view(["GET"])
def index(request):
    serializer = DiscordUserSerializer(request.user)
    #print(request.user)
    return Response(serializer.data)


def discord_login(request): 
    return redirect(redirect_url_discord)

def discord_logout(request):
    logout(request)
    return JsonResponse("Succesfully Logged out", safe=False)

def discord_login_redirect(request):
    code = request.GET.get('code')
    user = exchange_code(code)
    discord_user = authenticate(request, user=user)
    discord_user = list(discord_user).pop()
    login(request, discord_user)
    return redirect('index')


@login_required(login_url='login/')
@api_view(["GET"])
def formlist(request):
    if request.user:
        forms = FormCreate.objects.filter(userid=request.user)
        serializer = FormCreateSerializer(forms, many=True)
        return Response(serializer.data)
    return Response("You are not logged in!")

@login_required(login_url='login/')
@api_view(["GET"])
def responselist(request):
    response = FormResponse.objects.all()
    serializer = FormResponseSerializer(response, many=True)
    return Response(serializer.data)

@login_required(login_url='login/')
@api_view(["GET"])
def formresponse(request, FormName):
    form = FormCreate.objects.get(FormName=FormName, userid=request.user)
    response = FormResponse.objects.filter(form=form)
    serializer = FormResponseSerializer(response, many=True)
    return Response(serializer.data)

@login_required(login_url='login/')
@api_view(["POST"])
def formcreateresponse(request):
    serializer = FormCreateSerializer(data=request.data)
    
    if serializer.is_valid():
       form = serializer.data 
       form["userid"] = request.user
       newform = FormCreate()
       newform.id = form['id']
       newform.userid = form['userid']
       newform.FormName = form['FormName']
       newform.Formfields = form['Formfields']
       newform.save()
    
    return Response(serializer.data)


def exchange_code(code):
    data = {
        "client_id":os.getenv("CLIENT_ID"),
        "client_secret":os.getenv("CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/oauth2/login/redirect/", 
        "scope": "identify"
    }
    headers = {
        "Content-type": "application/x-www-form-urlencoded"
    }
    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    #print(response.json())
    credentials = response.json()
    access_token = credentials['access_token']
    response = requests.get("https://discord.com/api/v6/users/@me", headers={
        'Authorization': 'Bearer %s' % access_token
    })
    user = response.json()
    return user
