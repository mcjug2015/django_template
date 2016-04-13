''' module for extra urls '''
# pylint: disable=C0103
from django.conf.urls import include, url
from template_app.tests.selenium.extra_views import views


urlpatterns = [
    url(r'^', include('django_template.urls')),
    url(r'^selenium/create_user/', views.create_user),
    url(r'^selenium/remove_user/', views.remove_user),
    url(r'^selenium/create_shop/', views.create_shop),
]
