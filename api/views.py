from django.contrib.auth import authenticate
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
import jwt, json

# Create your views here.
from Passes.models import Pass
from Student.models import Student
from Teacher.models import Teacher

'''class PassView(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerialize'''


def home(request):
    return


@csrf_exempt  # DOESN'T WORK WITHOUT (NEED FOR EVERYTHING)
def post(request):
    print('go')
    try:
        for key in request.POST:
            print(key)
            value = request.POST[key]
            print(value)

        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
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

        # THIS IS THE TOKEN THAT IS PASSED AROUND WITH THE AUTHENTICATION DATA FROM MOBILE TO SERVER [REQUIRED]
        jwt_token = {'token': str(bytearray(jwt.encode(payload, "SECRET_KEY", algorithm='HS256')))}

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

@csrf_exempt  # DOESN'T WORK WITHOUT (NEED FOR EVERYTHING)
def model_update(request):
    print('here')
    print(request.POST.get('id'), request.POST.get('type'), request.POST.get('obj'))
    objType = request.POST.get('type')

    #try:
    print('there')
    if objType == 'student':
        obj = Student.objects.get(pk=request.POST.get('id'))
        serializers.deserialize('json', request.POST.get('obj'))
    elif objType == 'teacher':
        obj = Teacher.objects.get(pk=request.POST.get('id'))
        print('enw thing', serializers.deserialize('json', json.loads(request.POST.get('obj'))))
    elif objType == 'pass':
        print('anywhere')
        #PROBLEM SECTION: THE OBJ_GENERATOR WON'T ITERATE OR ANYTHING (I THINK IT ISN'T CREATING AN OBJECT BUT IDK)
        #TEST LINE (BASH): curl -d 'type=pass&id=10&obj={"model": "Passes.pass", "pk": 10, "fields": {"timeLeftOrigin": null, "destinationTeacher": 1, "description": "1", "location": null, "approved": true, "student": 2, "startTimeRequested": "2018-07-16T03:36:03Z", "type": "1", "endTimeRequested": "2018-07-16T03:36:04Z", "originTeacher": 1, "timeArrivedDestination": "2018-07-16T03:36:41.956Z"}}' -X POST http://127.0.0.1:8000/api/model_update/
        obj = Pass.objects.get(pk=request.POST.get('id'))
        obj_generator = serializers.json.Deserializer(json.loads(request.POST.get('obj')))
        print(obj_generator)
        for obja in obj_generator:
            print('booooo')
            obja.save()
    '''except:
        return HttpResponse(
            json.dumps({'Error': "Invalid request"}),
            status=400,
            content_type="application/json"
        )'''

    return HttpResponse(
        json.dumps({'Good': "good"}),
        status=200,
        content_type="application/json"
    )
'''
Takes a string of type = (student, teacher, pass) as string
and id of the element you want

returns the json form of the object you want
'''
@csrf_exempt  # DOESN'T WORK WITHOUT (NEED FOR EVERYTHING)
def model_request(request):
    print(request.POST.get('id'), request.POST.get('type'))
    objType = request.POST.get('type')

    try:
        if objType == 'student':
            obj = Student.objects.get(pk=request.POST.get('id'))
            obj = serializers.deserialize()
        elif objType == 'teacher':
            obj = Teacher.objects.get(pk=request.POST.get('id'))
        elif objType == 'pass':
            obj = Pass.objects.get(pk=request.POST.get('id'))
    except:
        return HttpResponse(
            json.dumps({'Error': "Invalid request"}),
            status=400,
            content_type="application/json"
        )

    data = serializers.serialize('json', [obj, ])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data, content_type='application/json')