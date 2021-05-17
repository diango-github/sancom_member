from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import Lan_appView, Eshadow, Esplite, Cshadow, Csplite, Lan_appView2
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Lan_appView.as_view(), name='sancomcontents'),
    url('eshadow/', Eshadow.as_view(), name='eshadow'),
    url('esplite/', Esplite.as_view(), name='esplite'),
    url('cshadow/', Cshadow.as_view(), name='cshadow'),
    url('csplite/', Csplite.as_view(), name='csplite'),
    url('publiccontents/', Lan_appView2.as_view(), name='publiccontents'),
]