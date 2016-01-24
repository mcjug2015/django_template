''' views module for template app '''
import json
from django.contrib.auth import authenticate, login
from django.http.response import JsonResponse


def login_async(request):
    ''' get username and password from json request body, log user in '''
    json_in = json.loads(request.body)
    username = json_in['username']
    password = json_in['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return JsonResponse({'status': 'good to go',
                                 'status_code': 200})
        else:
            return JsonResponse({'status': 'inactive user, go away',
                                 'status_code': 403})
    else:
        return JsonResponse({'status': 'wrong u/p',
                             'status_code': 403})
