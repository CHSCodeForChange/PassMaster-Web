from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework.response import Response
import jwt, json

# Create your views here.

'''class PassView(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerialize'''


def home(request):
    return


def post(request, username, password):
    print('go')
    try:
        user = authenticate(username=username, password=password)
        print(user)
    except User.DoesNotExist:
        print('error')
        return Response({'Error': "Invalid username/password"}, content_type="application/json",
                        status="400")
    if user:
        print('works')

        # TODO: CHANGE DEFAULTS
        payload = {
            'id': user.id,
            'email': 'booo',
        }

        jwt_token = {'token': str(bytearray(jwt.encode(payload, "SECRET_KEY",  algorithm='HS256')))}

        return HttpResponse(
            json.dumps(jwt_token),
            status=200,
            content_type="application/json"
        )
    else:
        print('sucks')
        return Response(
            json.dumps({'Error': "Invalid credentials"}),
            status=400,
            content_type="application/json"
        )
