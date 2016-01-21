# pylint: disable=C0103
"""the_template URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from tastypie.api import Api
from template_app.api import CigarShopResource, FaveShopsResource
from template_app.views import login_async


API_V1 = Api(api_name='v1')
API_V1.register(CigarShopResource())
API_V1.register(FaveShopsResource())


urlpatterns = [
    url(r'^welcome/', TemplateView.as_view(template_name='cigarshops/cigarshops.html')),
    url(r'^login_async/', login_async),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(API_V1.urls)),
]
