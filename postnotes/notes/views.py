import urllib
import json
import datetime
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import status
from jose import jwt

from postnotes.utilities import *
from models import *

target_audience = 'post-notes'
certificate_url = 'https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com'
response = urllib.urlopen(certificate_url)
certs = response.read()
certs = json.loads(certs)


def get_token_details(token):
    payload = jwt.decode(token, certs, algorithms='RS256', audience=target_audience)
    return payload


def get_or_create_user(payload):
    # Get the user from the database.
    # If they're not in the database, create them.
    try:
        user = User.objects.get(user_id=payload['user_id'])
        return user
    except ObjectDoesNotExist as e:
        user = User(user_id=payload['user_id'], name=payload['name'], email=payload['email'])
        user.save()
        return user


def get_request_user(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        # load the token from the header and parse it
        jwt_token = request.META['HTTP_AUTHORIZATION']
        try:
            payload = get_token_details(jwt_token)
            return get_or_create_user(payload)
        except jwt.JWTError as e:
            # invalid token!
            print 'Received error from jwt: ', e
            return None
    else:
        return None


class NotesHandler(APIView):
    def get(self, request, format=None):
        # Load the user
        user = get_request_user(request)
        if user is None:
            return HTTP_400('You must send a valid Firebase token to view your notes')
        # Get their notes as an array
        notes = [note.to_json() for note in Note.objects.filter(user=user)]
        # Wrap it in an object to make JsonResponse happy
        response = {'notes': notes}
        # Send the response
        return JsonResponse(data=response, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        user = get_request_user(request)
        if user is None:
            return HTTP_400('You must send a Firebase token to create notes')
        note_info = json.loads(request.body)
        if 'note' in note_info:
            n = Note(user=user, note_text=note_info['note'], create_date=datetime.datetime.now())
            n.save()
            return JsonResponse(data=n.to_json(), status=status.HTTP_200_OK)
        else:
            HTTP_400('The note text is missing.')
        pass
