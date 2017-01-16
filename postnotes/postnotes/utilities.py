from django.http import HttpResponse, JsonResponse
from rest_framework import status


def HTTP_200(data):
    return JsonResponse(data=data, status=status.HTTP_200_OK)


def HTTP_500(message):
    return JsonResponse(data={'msg': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def HTTP_400(message):
    return JsonResponse(data={'msg': message}, status=status.HTTP_400_BAD_REQUEST)


def HTTP_404(message):
    return JsonResponse(data={'msg': message}, status=status.HTTP_404_NOT_FOUND)
