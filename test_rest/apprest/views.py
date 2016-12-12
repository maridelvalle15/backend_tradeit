from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from apprest.models import *
from apprest.serializers import *
import json
from django.core import serializers


@csrf_exempt
def libro_list(request):
    """
    List all code libro, or create a new libro
    """
    if request.method == 'GET':
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LibroSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def libro_detail(request, pk):
    """
    Retrieve, update or delete a libro
    """
    try:
        libro = Libro.objects.get(pk=pk)
    except Libro.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = LibroSerializer(libro)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LibroSerializer(libro, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        libro.delete()
        return HttpResponse(status=204)


@api_view(['GET', 'POST'])
def post_user(request):
    print "hey"
    data = json.loads(request.body)
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    #r = {'is_claimed': 'True', 'rating': 3.5}
    #r = json.dumps(r)
    #response = json.loads(r)
    response = serializer.data
    return Response(response, status=200)


@api_view(['GET', 'POST', 'PUT'])
def get_user(request, id):
    data = JSONParser().parse(request)
    password = data['password']
    try:
        user = User.objects.get(username=id, password=password)
        serializer = UserSerializer(user)
        #r = {'is_claimed': 'True', 'rating': 3.5}
        #r = json.dumps(r)
        #response = json.loads(r)
        response = serializer.data
        return Response(response, status=200)
    except:
        return Response(status=400)


@csrf_exempt
@api_view(['PUT', 'GET', 'POST'])
def update_user(request, id):
    try:
        user = User.objects.get(username=id)
        data = JSONParser().parse(request)
        data['saldo'] = str(int(data['saldo']) + int(user.saldo))
        data['username'] = user.username
        data['password'] = user.password
        print data
        serializer = UserSerializer(user, data=data)
        print serializer
        if serializer.is_valid():
            print "im valid"
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    except:
        return Response(status=400)


@api_view(['POST', 'PUT'])
def transfer(request, id):
    data = JSONParser().parse(request)
    print data
    user_origin = User.objects.get(username=id)
    user_destination = User.objects.get(username=data['destination'])
    user_origin.saldo = str(int(user_origin.saldo) - int(data['amount']))
    user_destination.saldo = str(int(user_destination.saldo) + int(data['amount']))
    data['origin'] = user_origin.username
    serializer = TransaccionSerializer(data=data)
    if int(user_origin.saldo) < 0:
        return Response(status=400)
    else:
        if serializer.is_valid():
            print "im valid"
            serializer.save()
            user_origin.save()
            user_destination.save()
            data['amount'] = user_origin.saldo
            return JsonResponse(data)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
def get_transactions(request):
    transactions = Transaccion.objects.all()
    serializer = TransaccionSerializer(transactions, many=True)
    #r = {'is_claimed': 'True', 'rating': 3.5}
    #r = json.dumps(r)
    #response = json.loads(r)
    response = serializer.data
    print response
    return Response(response, status=200)
