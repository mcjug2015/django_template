''' extra views for selenium tests '''
import json
from django.contrib.auth.models import User
from django.utils import timezone
from django.http.response import JsonResponse, HttpResponse
from django.contrib.gis.geos.factory import fromstr
from template_app.models import CigarShop


def create_user(request):
    ''' create a new user  '''
    username = request.GET['username']
    last_id = User.objects.all().order_by("-id")[0].pk
    the_user = User(username=username, email="%s@test.com" % username,
                    last_login=timezone.now(), is_active=True, id=last_id+1)
    the_user.set_password("selenium_password")
    the_user.save()
    return JsonResponse({'username': username, 'password': "selenium_password"})


def remove_user(request):
    ''' remove a user from the db '''
    username = request.GET['username']
    if User.objects.filter(username=username).count() > 0:
        User.objects.filter(username=username).delete()
        return HttpResponse(content="%s removed" % username)
    return HttpResponse(content="%s wasn't in the db" % username)


def create_shop(request):
    ''' create a cigarshop no auth '''
    json_in = json.loads(request.body)
    the_user = User.objects.get(username=json_in['username'])
    cigar_shop = CigarShop(name=json_in['name'],
                           location=fromstr('POINT(%s %s)' % (float(json_in['long']),
                                                              float(json_in['lat'])), srid=4326),
                           owner=the_user)
    cigar_shop.save()
    return JsonResponse({'new_shop_id': cigar_shop.pk})
