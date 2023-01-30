from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from datetime import datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import AdvocateSerializer, CompanySerializer
from django.db.models import Q
# import the below for api view for function based view
from rest_framework.decorators import api_view, permission_classes
# import the below for api view for class based view
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import requests_oauthlib
import autsecrets
from dotenv import load_dotenv
load_dotenv()

import os
import json

#New edits
import tweepy
import re
import time

# TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
# TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')
# TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
# TWITTER_ACCESS_TOKEN_SECRET  = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET ')
# BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

TWITTER_API_KEY= requests_oauthlib.OAuth1(os.environ.get('TWITTER_API_KEY'))
# TWITTER_API_SECRET = autsecrets.TWITTER_API_SECRET
# TWITTER_ACCESS_TOKEN = autsecrets.TWITTER_ACCESS_TOKEN
# TWITTER_ACCESS_TOKEN_SECRET  = autsecrets.TWITTER_ACCESS_TOKEN_SECRET
# BEARER_TOKEN = autsecrets.BEARER_TOKEN


# Create your views here.
# def endpoints(request):
#     data = ['/advocates', '/advocates/:username']
#     return JsonResponse(data, safe=False)

# def advocates_list(request):
#     data = ['Dennis', 'Travas', 'Ivanov', 'Obapythonaire']
#     return JsonResponse(data, safe=False)

# def advocate_detail(request, username):
#     data = username
#     return JsonResponse(data, safe=False)

# Authentications
auth = requests_oauthlib.OAuth1(autsecrets.TWITTER_API_KEY,
                                autsecrets.TWITTER_API_SECRET,
                                autsecrets.TWITTER_ACCESS_TOKEN,
                                autsecrets.TWITTER_ACCESS_TOKEN_SECRET)

auth2 = tweepy.OAuth1UserHandler(autsecrets.TWITTER_API_KEY,
                                autsecrets.TWITTER_API_SECRET,
                                autsecrets.TWITTER_ACCESS_TOKEN,
                                autsecrets.TWITTER_ACCESS_TOKEN_SECRET)

# auth = requests_oauthlib.OAuth1(os.environ.get('TWITTER_API_KEY'),
#     os.environ.get('TWITTER_API_SECRET'),
#     os.environ.get('TWITTER_ACCESS_TOKEN'),
#     os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

# auth2 = tweepy.OAuth1UserHandler(os.environ.get('TWITTER_API_KEY'),
#     os.environ.get('TWITTER_API_SECRET'),
#     os.environ.get('TWITTER_ACCESS_TOKEN'),
#     os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

@api_view(['GET'])
def endpoints(request):
    # print('TWITTER API KEY:', TWITTER_API_KEY)
    data = ['/advocates', '/advocates/:username']
    context = {'data': 'data'}
    return Response(data)

@api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
def advocates_list(request):
    # data = ['Dennis', 'Travas', 'Ivanov', 'Obapythonaire']
    api = tweepy.API(auth2)
    if request.method == 'GET':
        query = request.GET.get('query')

        if query == None:
            query = ''
        advocates  = Advocate.objects.filter(Q(username__icontains=query)| Q(bio__icontains=query))
        # advocates = Advocate.objects.filter(username='').delete()
        # advocates.save()
        # Start of my editing
        # api = tweepy.API(auth2)
        # users = []
        # for user in tweepy.Cursor(api.search_users, q='"developer advocates" OR "developer"').items(4):
        #     #print(f"@{user.screen_name} - {user.description}")
        #     time.sleep(1.0 / 1000)  # Pause execution for 1/1000 of a second
        #     users.append(user)
        #     name = user.name
        #     user_name = user.screen_name
        #     bio = user.description
        #     twitter = 'https://twitter.com/' + f"{user_name}"
        #     profile_pic_crude = user.profile_image_url
        #     profile_pic =profile_pic_crude.replace('normal', '400x400')

        #     print(f"Name: {name} Twitter Username: {user_name} Bio: {bio} url: {twitter} ppic: {profile_pic}")
            # response = json.dumps(users, default=vars)
            # users_iterator = iter(users)
            # response = dict(zip(users_iterator, users_iterator))
            # name = response['screen_name']
            # # print(type(users))
            # print(name)
            # print(type(response))
            # user.profile_pic = user['profile_image_url'].replace('normal', '400x400')
            # for advocate in user:
            #     advocate.username = username = user('username')
            #     advocate.name = user['name']
            #     advocate.profile_pic = user['profile_image_url'].replace('normal', '400x400')
            #     advocate.bio = user['description']
            #     advocate.twitter = 'https://twitter.com/' + username
            # data = user['data']
            # serializer = AdvocateSerializer(user, many=False)
            # print(serializer)
            # return Response(serializer.data)
            # print(response)
            # print(f"@{user.screen_name} - {user.description} - {user.name} - {user.profile_pic}")
            
        # My editing ends here

        # advocates = Advocate.objects.all()
        serializer = AdvocateSerializer(advocates, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        # new_users =[]
        for user in tweepy.Cursor(api.search_users, q='"software" OR "developer"').items(10):
            time.sleep(1.0 / 1000)  # Pause execution for 1/1000 of a second
            username = user.screen_name
            joined_at = user.created_at
            # print(user)

            # for new_user in user:
            #     username = new_user.screen_name        
            # if Advocate.objects.filter(username=username).exists():
                # break
                # return Response({"error": "User already exists."}, status=status.HTTP_400_BAD_REQUEST)

            advocate = Advocate.objects.create(         
            username = user.screen_name,
            name =user.name,
            bio = user.description,
            twitter = 'https://twitter.com/' + username,
            profile_pic =user.profile_image_url.replace('normal', '400x400'),
            followers = user.followers_count,
            joined = datetime.strftime(joined_at, '%Y-%m-%d')
            )
            
            # if Advocate.objects.filter(username=username).exists():
                # break
        # else:
            # if Advocate.objects.filter(username=username).exists():
                # return Response({"error": "User already exists."}, status=status.HTTP_400_BAD_REQUEST)
    # print(advocate)
    advocate.save()
    print("Advocates saved")  
    serializer = AdvocateSerializer(advocate, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)     

# Writing advocate_detail in Class based view

class AdvocateDetail(APIView):
    # To avoid querying the advocate list everytime, we use a function
    def get_object(self, username):
        try:
            return Advocate.objects.get(username=username)
        except Advocate.DoesNotExist:
            raise JsonResponse('Advocate does not exist')

    def get(self, request, username):
        # try:
        # This method wprked but it means I will be gettng user info directly
        # from the database, fine and good but,
        # If I add a user manually, it won't update the user data except i update all manually
        #  

        # advocate = Advocate.objects.get(username=username)
        # serializer = AdvocateSerializer(advocate, many=False)
        # return Response(serializer.data)


        # except Advocate.DoesNotExist:
            # raise JsonResponse('Advocate does not exist')
        # advocate = self.get_object(username)
        # advocate = Advocate.objects.get(username)    

        head = {'Authorization': 'Bearer' + TWITTER_API_KEY}

        fields = '?user.fields=profile_image_url,description,public_metrics,created_at'

        url = "https://api.twitter.com/2/users/by/username/" + str(username) + fields
        response = requests.get(url, headers=head).json()
        # response = requests.get(url, auth=auth).json()
        # print(response)
        data = response['data']
        data['profile_image_url'] = data['profile_image_url'].replace('normal', '400x400')

        print('DATA FROM TWITTER:', data)

        advocate = self.get_object(username)
        advocate.name = data['name']
        advocate.followers = data['public_metrics']['followers_count']
        advocate.joined = data['created_at'][:10]
        advocate.profile_pic = data['profile_image_url']
        advocate.bio = data['description']
        advocate.twitter = 'https://twitter.com/' + username
        # print(advocate.name)

        advocate.save()
        # advocate = Advocate.objects.get(username=username)
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
        # return Response(data)
        # return Response('username')
    def put(self, request, username):
        advocate = self.get_object(username)
        # advocate = Advocate.objects.get(username=username)
        advocate.username = request.data['username']
        advocate.bio = request.data['bio']
        advocate.name = request.data['name']
        advocate.followers = request.data['public_metrics']['followers_count']
        advocate.joined = request.data['created_at'][:10]
        advocate.profile_pic = request.data['profile_image_url']
        advocate.twitter = 'https://twitter.com/' + username

        advocate.save()
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

    def delete(self, request, username):
        advocate = self.get_object(username)
        # advocate = Advocate.objects.get(username=username)

        advocate.delete()
        return Response('User Successfully Deleted')

# @api_view(['GET', 'PUT', 'DELETE'])
# def advocate_detail(request, username):
    # data = username
    # advocate = Advocate.objects.get(username=username)
    # if request.method == 'GET':
    #     serializer = AdvocateSerializer(advocate, many=False)
    #     return Response(serializer.data)

    # if request.method == 'PUT':
    #     advocate.username = request.data['username']
    #     advocate.bio = request.data['bio']

    #     advocate.save()

    #     serializer = AdvocateSerializer(advocate, many=False)
    #     return Response(serializer.data)

    # if request.method == 'DELETE':
    #     # advocate.username = request.data['username']
    #     # advocate.bio = request.data['bio']

    #     advocate.delete()

    #     # serializer = AdvocateSerializer(advocate, many=False)
    #     # return Response(serializer.data)
    #     return Response("user was deleted")

@api_view(['GET','POST'])
def companies_list(request):
    companies = Company.objects.all()


    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)
    